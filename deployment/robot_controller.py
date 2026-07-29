#!/usr/bin/env python3

# Pioneer P3-DX / MobileSim 

from __future__ import annotations

import glob
import math
import os
import socket
import struct
import threading
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


# Optional deps
try:
    import serial  # type: ignore
    try:
        from serial.tools import list_ports  # type: ignore
    except Exception:
        list_ports = None
except Exception:
    serial = None
    list_ports = None


# ============================================================
# CONFIG
# ============================================================

DEFAULT_SERIAL_PORT = os.environ.get("P3DX_SERIAL", "COM3" if os.name == "nt" else "/dev/ttyUSB0")
SERIAL_BAUD = int(os.environ.get("P3DX_BAUD", "9600"))

MOBILE_SIM_HOST = os.environ.get("P3DX_HOST", "127.0.0.1")
MOBILE_SIM_PORT = int(os.environ.get("P3DX_PORT", "8101"))

# Waypoints (mm) relative to start
NODES_REL_ALL: List[Tuple[float, float]] = [
    (0.0, 0.0),
    (2060.0, 0.0),
]
NODES_ODOM: List[Tuple[float, float]] = NODES_REL_ALL[1:]

CONTROL_HZ = 20
WATCHDOG_SEC = 1.0

MAX_V_MM_S = 300
MAX_W_DEG_S = 60

# Avoidance thresholds (mm)
AVOID_GAMMA_A_MM = 150.0


# ============================================================
# Helpers
# ============================================================

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def wrap_deg_180(a: float) -> float:
    return (a + 180.0) % 360.0 - 180.0


def deg360(th: float) -> float:
    return th - 360.0 * math.floor(th / 360.0)


def list_serial_ports_manual() -> List[str]:
    """
    Manual port list for Real Robot mode.
    Uses pyserial list_ports if available (best for Windows).
    """
    ports: List[str] = []
    if list_ports is not None:
        try:
            for p in list_ports.comports():
                if p.device:
                    ports.append(p.device)
        except Exception:
            pass

    # Fallback (still manual list, NOT auto-trying them)
    if not ports:
        if os.name == "nt":
            ports = [f"COM{i}" for i in range(1, 21)]
        else:
            for pat in ("/dev/serial/by-id/*", "/dev/serial/by-path/*", "/dev/ttyUSB*", "/dev/ttyACM*"):
                ports += sorted(glob.glob(pat))

    # unique
    seen = set()
    out = []
    for p in ports:
        if p not in seen:
            out.append(p)
            seen.add(p)
    return out


# ============================================================
# P2OS / ARIA protocol basics
# ============================================================

HEADER = bytes([0xFA, 0xFB])

SYNC0 = bytes([0xFA, 0xFB, 0x03, 0x00, 0x00, 0x00])
SYNC1 = bytes([0xFA, 0xFB, 0x03, 0x01, 0x00, 0x01])
SYNC2 = bytes([0xFA, 0xFB, 0x03, 0x02, 0x00, 0x02])

CMD_PULSE = 0
CMD_OPEN = 1
CMD_ENABLE = 4
CMD_VEL = 11
CMD_RVEL = 21
CMD_SONAR = 28
CMD_STOP = 29

ARG_POS_INT = 0x3B
ARG_NEG_INT = 0x1B


def calc_checksum(packet: bytes) -> int:
    c = 0
    i = 3
    n = packet[2] - 2
    while n > 1:
        c += (packet[i] << 8) | packet[i + 1]
        c &= 0xFFFF
        n -= 2
        i += 2
    if n > 0:
        c ^= packet[i]
    return c & 0xFFFF


# ============================================================
# SIP parsing
# ============================================================

@dataclass
class RobotState:
    x_mm: float = 0.0
    y_mm: float = 0.0
    th_deg_wrap: float = 0.0
    th_deg_360: float = 0.0

    left_vel_mm_s: float = 0.0
    right_vel_mm_s: float = 0.0

    v_mm_s: float = 0.0
    w_deg_s: float = 0.0

    sonars_mm: List[float] = None

    def __post_init__(self):
        if self.sonars_mm is None:
            self.sonars_mm = [0.0] * 16


def _i16_le(buf: bytes, off: int) -> int:
    return struct.unpack_from("<h", buf, off)[0]


def parse_sip(packet: bytes, prev_sonars: List[float]) -> Optional[Tuple[float, float, float, float, float, List[float]]]:
    if len(packet) < 6 or packet[:2] != HEADER:
        return None
    bytecount = packet[2]
    if len(packet) < 3 + bytecount:
        return None

    payload = packet[3:3 + bytecount]
    if len(payload) < 5:
        return None

    data = payload[1:-2]
    if len(data) < 2 * 5 + 1 + 2 * 3 + 1 + 1:
        return None

    off = 0
    x_raw = float(_i16_le(data, off)); off += 2
    y_raw = float(_i16_le(data, off)); off += 2
    th_raw = float(_i16_le(data, off)); off += 2
    lvel = float(_i16_le(data, off)); off += 2
    rvel = float(_i16_le(data, off)); off += 2

    _battery = data[off]; off += 1
    _stall = _i16_le(data, off); off += 2
    _control = _i16_le(data, off); off += 2
    _flags = _i16_le(data, off); off += 2
    _compass = data[off]; off += 1
    sonar_count = int(data[off]); off += 1

    sonars = prev_sonars[:] if prev_sonars else [0.0] * 16
    for _ in range(sonar_count):
        if off + 3 > len(data):
            break
        sn = int(data[off]); off += 1
        sr = float(_i16_le(data, off)); off += 2
        if 0 <= sn < len(sonars):
            sonars[sn] = sr

    return x_raw, y_raw, th_raw, lvel, rvel, sonars


# ============================================================
# Link layer (TCP + Serial explicit)
# ============================================================

class PioneerRobot:
    def __init__(self):
        self.use_serial = False
        self.sock: Optional[socket.socket] = None
        self.ser = None

        self._rx_thread: Optional[threading.Thread] = None
        self._stop_evt = threading.Event()
        self._buf = bytearray()

        self._lock = threading.Lock()
        self._latest: Optional[RobotState] = None

        self._origin_set = False
        self._x0 = 0.0
        self._y0 = 0.0
        self._th0 = 0.0
        self._sonars = [0.0] * 16

        self._last_pulse = 0.0

        self.endpoint = ""
        self.transport = ""

    def _theta_raw_to_deg(self, th_raw: float) -> float:
        # Both the simulator and the physical hardware 
        # send heading data as an integer between 0 and 4095 ticks per revolution.
        # if self.use_serial:
        #     return float(th_raw) / 10.0
        return float(th_raw) * 360.0 / 4095.0

    def _write(self, b: bytes) -> None:
        try:
            if self.use_serial and self.ser is not None:
                self.ser.write(b)
            elif self.sock is not None:
                self.sock.sendall(b)
        except Exception as e:
            print(f"[WARN] write failed ({e}); disconnecting")
            self.close()

    def _read_some(self) -> bytes:
        if self.use_serial and self.ser is not None:
            return self.ser.read(4096)
        if self.sock is not None:
            try:
                data = self.sock.recv(4096)
                if data == b"":
                    raise ConnectionError("TCP closed")
                return data
            except socket.timeout:
                return b""
        return b""

    def _start_reader_and_wait_sip(self, timeout_s: float = 0.9) -> bool:
        self._stop_evt.clear()
        self._rx_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._rx_thread.start()

        self._origin_set = False
        with self._lock:
            self._latest = None
        self._last_pulse = time.time()

        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if self.get_state() is not None:
                return True
            time.sleep(0.02)
        return False

    def connect_tcp(self, host: str, port: int) -> bool:
        self.close()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2.0)
            self.sock.connect((host, port))
            self.sock.settimeout(0.05)
            self.use_serial = False
            self.transport = "tcp"
            self.endpoint = f"{host}:{port}"
            print(f"[OK] TCP connected: {self.endpoint}")
        except Exception as e:
            print(f"[ERR] TCP connect failed: {e}")
            self.sock = None
            return False

        if not self._handshake():
            self.close()
            return False

        if not self._start_reader_and_wait_sip():
            print("[ERR] TCP connected but no SIP received (MobileSim not streaming?)")
            self.close()
            return False

        return True

    def connect_serial(self, port: str, baud: int) -> bool:
        self.close()
        if serial is None:
            print("[ERR] pyserial not installed; cannot use Serial")
            return False
        try:
            self.ser = serial.Serial(port, baud, timeout=0.05)
            self.use_serial = True
            self.transport = "serial"
            self.endpoint = f"{port} @ {baud}"
            print(f"[OK] Serial connected: {self.endpoint}")
        except Exception as e:
            print(f"[ERR] Serial connect failed: {e}")
            self.ser = None
            return False

        if not self._handshake():
            self.close()
            return False

        if not self._start_reader_and_wait_sip():
            print("[ERR] Serial connected but no SIP received (wrong port/baud?)")
            self.close()
            return False

        return True

    def close(self) -> None:
        self._stop_evt.set()
        try:
            self.stop_motion()
        except Exception:
            pass

        try:
            if self.ser is not None:
                self.ser.close()
        except Exception:
            pass

        try:
            if self.sock is not None:
                self.sock.close()
        except Exception:
            pass

        self.ser = None
        self.sock = None
        self.use_serial = False

        with self._lock:
            self._latest = None

    def is_connected(self) -> bool:
        return self.ser is not None or self.sock is not None

    def send_cmd(self, cmd: int, arg: Optional[int] = None) -> None:
        if arg is None:
            bytecount = 1 + 2
            pkt_wo = HEADER + bytes([bytecount]) + bytes([cmd])
            chk = calc_checksum(pkt_wo + b"\x00\x00").to_bytes(2, "big")
            self._write(pkt_wo + chk)
            return

        if arg < 0:
            argtype = ARG_NEG_INT
            aval = abs(int(arg))
        else:
            argtype = ARG_POS_INT
            aval = int(arg)

        arg_bytes = struct.pack("<H", aval & 0xFFFF)
        bytecount = 1 + 1 + 2 + 2
        pkt_wo = HEADER + bytes([bytecount]) + bytes([cmd, argtype]) + arg_bytes
        chk = calc_checksum(pkt_wo + b"\x00\x00").to_bytes(2, "big")
        self._write(pkt_wo + chk)

    def _handshake(self) -> bool:
        try:
            for p in (SYNC0, SYNC1, SYNC2):
                self._write(p)
                time.sleep(0.05)
                _ = self._read_some()

            self.send_cmd(CMD_OPEN)
            self.send_cmd(CMD_ENABLE, 1)
            self.send_cmd(CMD_SONAR, 1)
            self.send_cmd(CMD_PULSE)
            print("[OK] Handshake done (SYNC/OPEN/ENABLE/SONAR)")
            return True
        except Exception as e:
            print(f"[ERR] Handshake failed: {e}")
            return False

    def _reader_loop(self) -> None:
        while not self._stop_evt.is_set():
            try:
                data = self._read_some()
                if data:
                    self._buf.extend(data)
                    self._consume_packets()
                else:
                    time.sleep(0.01)
            except Exception as e:
                print(f"[WARN] reader stopped ({e}); disconnecting")
                self.close()
                break

    def _consume_packets(self) -> None:
        while True:
            if len(self._buf) < 4:
                return

            h = self._buf.find(HEADER)
            if h < 0:
                self._buf.clear()
                return
            if h > 0:
                del self._buf[:h]
                if len(self._buf) < 4:
                    return

            bytecount = self._buf[2]
            total_len = 3 + bytecount
            if len(self._buf) < total_len:
                return

            pkt = bytes(self._buf[:total_len])
            del self._buf[:total_len]

            ptype = pkt[3] if len(pkt) > 3 else 0
            if not (0x30 <= ptype <= 0x33):
                continue

            parsed = parse_sip(pkt, self._sonars)
            if parsed is None:
                continue

            x_raw, y_raw, th_raw, lvel, rvel, sonars = parsed
            th_deg_abs = self._theta_raw_to_deg(th_raw)
            self._sonars = sonars[:]

            if not self._origin_set:
                self._origin_set = True
                self._x0, self._y0, self._th0 = x_raw, y_raw, th_deg_abs

            x_rel = x_raw - self._x0
            y_rel = y_raw - self._y0
            th_rel = th_deg_abs - self._th0

            st = RobotState(
                x_mm=x_rel,
                y_mm=y_rel,
                th_deg_wrap=wrap_deg_180(th_rel),
                th_deg_360=deg360(th_rel),
                left_vel_mm_s=lvel,
                right_vel_mm_s=rvel,
                v_mm_s=(lvel + rvel) / 2.0,
                w_deg_s=(rvel - lvel) * 0.1,
                sonars_mm=sonars[:],
            )
            with self._lock:
                self._latest = st

    def get_state(self) -> Optional[RobotState]:
        with self._lock:
            if self._latest is None:
                return None
            s = self._latest
            return RobotState(
                x_mm=s.x_mm,
                y_mm=s.y_mm,
                th_deg_wrap=s.th_deg_wrap,
                th_deg_360=s.th_deg_360,
                left_vel_mm_s=s.left_vel_mm_s,
                right_vel_mm_s=s.right_vel_mm_s,
                v_mm_s=s.v_mm_s,
                w_deg_s=s.w_deg_s,
                sonars_mm=s.sonars_mm[:],
            )
        
    def get_pose(self):
            st = self.get_state()

            if st is None:
                return None

            origin_x = getattr(self, "_origin_x", 0.0)
            origin_y = getattr(self, "_origin_y", 0.0)
            origin_heading = getattr(self, "_origin_heading", 0.0)

            return (
                st.x_mm - origin_x,
                st.y_mm - origin_y,
                wrap_deg_180(st.th_deg_360 - origin_heading),
            )
    def drive(self, v_mm_s: float, w_deg_s: float) -> None:
        v = int(clamp(v_mm_s, -MAX_V_MM_S, MAX_V_MM_S))
        w = int(clamp(w_deg_s, -MAX_W_DEG_S, MAX_W_DEG_S))
        self.send_cmd(CMD_VEL, v)
        self.send_cmd(CMD_RVEL, w)

    def stop_motion(self) -> None:
        self.send_cmd(CMD_STOP)
        self.send_cmd(CMD_VEL, 0)
        self.send_cmd(CMD_RVEL, 0)
    
    def move_forward(self, speed: float = 200.0) -> None:
        self.drive(speed, 0.0)

    def move_backward(self, speed: float = 150.0) -> None:
        self.drive(-abs(speed), 0.0)

    def turn_left(self, speed_deg_s: float = 35.0) -> None:
        self.drive(0.0, abs(speed_deg_s))

    def turn_right(self, speed_deg_s: float = 35.0) -> None:
        self.drive(0.0, -abs(speed_deg_s))

    def stop(self) -> None:
        self.stop_motion()

    def rotate_to_heading(
        self,
        target_heading: float,
        tolerance: float = 2.0,
        speed_deg_s: float = 25.0,
        timeout_s: float = 10.0,
    ) -> bool:
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout_s:
                self.stop()
                return False

            st = self.get_state()

            if st is None:
                self.stop()
                return False

            error = wrap_deg_180(target_heading - st.th_deg_360)

            if abs(error) <= tolerance:
                self.stop()
                return True

            if error > 0:
                self.turn_left(speed_deg_s)
            else:
                self.turn_right(speed_deg_s)

            time.sleep(0.02)

    def move_distance(
        self,
        distance_mm: float,
        speed_mm_s: float = 200.0,
        tolerance_mm: float = 20.0,
    ) -> bool:
        

        start = self.get_state()

        if start is None:
            return False

        start_x = start.x_mm
        start_y = start.y_mm

        direction = 1 if distance_mm >= 0 else -1

        start_time = time.time()

        while True:

            if time.time() - start_time > 15:
                self.stop()
                return False

            st = self.get_state()

            if st is None:
                self.stop()
                return False

            travelled = math.hypot(
                st.x_mm - start_x,
                st.y_mm - start_y,
            )

            if travelled >= abs(distance_mm) - tolerance_mm:
                self.stop()
                return True

            self.drive(direction * speed_mm_s, 0)

            time.sleep(0.02)


    def reset_odometry(self) -> bool:
   
        st = self.get_state()

        if st is None:
            return False

        self._origin_x = st.x_mm
        self._origin_y = st.y_mm
        self._origin_heading = st.th_deg_360

        return True
    
    
    def pulse_if_needed(self) -> None:
        now = time.time()
        if now - self._last_pulse >= WATCHDOG_SEC:
            try:
                self.send_cmd(CMD_PULSE)
            except Exception:
                pass
            self._last_pulse = now




# ============================================================
# Behaviours
# ============================================================

class LabOdometryNavigator:
    KP_ROTATION = 0.4
    # KP_STEERING = 1.5

    CRUISE_SPEED = 300.0
    TURN_SPEED = 100.0
    BLEND_DIST = 150.0
    FINAL_DIST = 50.0

    MAX_ALIGN_W = 50.0
    MIN_ALIGN_W = 10.0
    MAX_STEER_W = 60.0

    def __init__(self, nodes: List[Tuple[float, float]]):
        self.nodes = nodes[:]
        self.i = 0

    def reset(self):
        self.i = 0

    def done(self) -> bool:
        return self.i >= len(self.nodes)

    def current_goal(self) -> Optional[Tuple[float, float]]:
        return None if self.done() else self.nodes[self.i]

    @staticmethod
    def _angle_to_goal_deg360(st: RobotState, gx: float, gy: float) -> float:
        deg = math.degrees(math.atan2(gy - st.y_mm, gx - st.x_mm))
        if deg < 0:
            deg += 360.0
        return deg

    def step(self, st: RobotState) -> Tuple[float, float, str]:
        if self.done():
            return 0.0, 0.0, "ODOM: DONE"

        gx, gy = self.nodes[self.i]
        dist = math.hypot(gx - st.x_mm, gy - st.y_mm)

        is_last = (self.i == len(self.nodes) - 1)
        hit = self.FINAL_DIST if is_last else self.BLEND_DIST

        if dist <= hit:
            if is_last:
                self.i = len(self.nodes)
                return 0.0, 0.0, "ODOM: FINISH"
            self.i += 1
            return 0.0, 0.0, f"ODOM: next waypoint ({self.i}/{len(self.nodes)})"

        target = self._angle_to_goal_deg360(st, gx, gy)
        err = wrap_deg_180(target - st.th_deg_360)

        if abs(err) > 3.5:
            w = clamp(err * self.KP_ROTATION, -self.MAX_ALIGN_W, self.MAX_ALIGN_W)
            if abs(w) < self.MIN_ALIGN_W:
                w = self.MIN_ALIGN_W if w > 0 else -self.MIN_ALIGN_W
            return 0.0, w, f"ODOM: ALIGN err={err:.1f}"

        # steer = clamp(err * self.KP_STEERING, -self.MAX_STEER_W, self.MAX_STEER_W)
        steer = 0.0
        speed = self.CRUISE_SPEED
        return speed, steer, f"ODOM: MOVE dist={dist:.0f}"



