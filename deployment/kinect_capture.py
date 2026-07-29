import argparse
import time
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image


class KinectCapture:
    """
    Capture interface for deployment.

    mode="opencv":
        Reads from cv2.VideoCapture. Useful for webcam testing.

    mode="file":
        Reads latest Kinect SDK frames from:
        deployment/live/rgb.png
        deployment/live/depth.bin
    """

    def __init__(
        self,
        camera_index: int = 1,
        width: int = 640,
        height: int = 480,
        mode: str = "opencv",
        live_dir: str = "deployment/live",
    ):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.mode = mode.lower().strip()
        self.live_dir = Path(live_dir)

        self.rgb_path = self.live_dir / "rgb.png"
        self.depth_path = self.live_dir / "depth.bin"

        self.cap: Optional[cv2.VideoCapture] = None

    def open(self) -> bool:
        if self.mode == "file":
            self.live_dir.mkdir(parents=True, exist_ok=True)
            print(f"[OK] File capture mode using: {self.live_dir}")
            print(f"Waiting for: {self.rgb_path}")
            print(f"Waiting for: {self.depth_path}")
            return True

        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print(f"[ERR] Could not open camera index {self.camera_index}")
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        print(f"[OK] Camera opened at index {self.camera_index}")
        return True

    def read_rgb(self) -> Optional[np.ndarray]:
        if self.mode == "file":
            if not self.rgb_path.exists():
                return None

            try:
                img = Image.open(self.rgb_path).convert("RGB")
                return np.array(img)
            except Exception as e:
                print(f"[WARN] Failed to read RGB frame: {e}")
                return None

        if self.cap is None or not self.cap.isOpened():
            return None

        ok, frame_bgr = self.cap.read()

        if not ok or frame_bgr is None:
            return None

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return frame_rgb

    def read_rgbd(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        if self.mode == "file":
            try:
                if not self.rgb_path.exists() or not self.depth_path.exists():
                    return None, None

                if self.depth_path.stat().st_size != 640 * 480 * 2:
                    return None, None

                rgb = Image.open(self.rgb_path).convert("RGB")
                rgb_frame = np.array(rgb)

                depth_raw = np.fromfile(self.depth_path, dtype=np.uint16)

                if depth_raw.size != 640 * 480:
                    return None, None

                depth_frame = depth_raw.reshape((480, 640)).astype(np.float32)

                return rgb_frame, depth_frame

            except Exception as e:
                print(f"[WARN] Failed to read RGB-D frame: {e}")
                return None, None

        rgb_frame = self.read_rgb()

        if rgb_frame is None:
            return None, None

        h, w = rgb_frame.shape[:2]
        fake_depth = np.ones((h, w), dtype=np.float32) * 1000.0

        return rgb_frame, fake_depth

    def read_rgb_bgr_for_display(self) -> Optional[np.ndarray]:
        rgb = self.read_rgb()

        if rgb is None:
            return None

        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()

    def __enter__(self):
        if not self.open():
            raise RuntimeError("Could not open KinectCapture source.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def test_camera(camera_index: int = 1, mode: str = "opencv", live_dir: str = "deployment/live") -> None:
    camera = KinectCapture(camera_index=camera_index, mode="file", live_dir=live_dir)

    if not camera.open():
        return

    print("Press Q to quit camera test.")

    try:
        while True:
            frame_bgr = camera.read_rgb_bgr_for_display()

            if frame_bgr is None:
                print("[WARN] No RGB frame received.")
                time.sleep(0.1)
                continue

            cv2.imshow("RGB Test", frame_bgr)

            key = cv2.waitKey(1) & 0xFF

            if key in (ord("q"), ord("Q"), 27):
                break

    finally:
        camera.close()


def main():
    parser = argparse.ArgumentParser(description="Test Kinect/OpenCV or file-based capture.")
    parser.add_argument("--camera", type=int, default=1)
    parser.add_argument("--mode", choices=["opencv", "file"], default="opencv")
    parser.add_argument("--live-dir", default="deployment/live")

    args = parser.parse_args()
    test_camera(args.camera, args.mode, args.live_dir)


if __name__ == "__main__":
    main()