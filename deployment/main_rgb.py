import argparse
import time

from kinect_capture import KinectCapture
from deploy_rgb import load_rgb_model, predict_rgb_mask, decide_navigation
from navigation import GlassNavigationController
from robot_controller import PioneerRobot, MOBILE_SIM_HOST, MOBILE_SIM_PORT, SERIAL_BAUD


def connect_robot(args):
    robot = PioneerRobot()

    if args.sim:
        ok = robot.connect_tcp(args.host, args.port)
    else:
        ok = robot.connect_serial(args.serial, args.baud)

    if not ok:
        raise RuntimeError("Failed to connect to Pioneer robot.")

    robot.reset_odometry()
    return robot


def main():
    parser = argparse.ArgumentParser(description="Live RGB_004 glass detection and Pioneer navigation.")

    parser.add_argument("--camera", type=int, default=1, help="Camera index for Kinect RGB stream.")
    parser.add_argument("--sim", action="store_true", help="Use MobileSim TCP instead of real robot serial.")
    parser.add_argument("--host", default=MOBILE_SIM_HOST)
    parser.add_argument("--port", type=int, default=MOBILE_SIM_PORT)
    parser.add_argument("--serial", default="COM3")
    parser.add_argument("--baud", type=int, default=SERIAL_BAUD)

    parser.add_argument("--max-frames", type=int, default=0, help="0 means run continuously.")
    parser.add_argument("--delay", type=float, default=0.05, help="Loop delay in seconds.")

    args = parser.parse_args()

    print("Loading RGB_004 model...")
    model, cfg, device, image_size = load_rgb_model()
    print(f"Model loaded on {device}")

    robot = connect_robot(args)
    navigator = GlassNavigationController(robot)

    camera = KinectCapture(camera_index=args.camera, mode="file")

    if not camera.open():
        robot.stop()
        robot.close()
        raise RuntimeError("Failed to open camera.")

    print("System running. Press Ctrl+C to stop.")

    frame_count = 0
    run_start_time = time.time()
    try:
        while True:
            robot.pulse_if_needed()

            rgb_frame = camera.read_rgb()
            

            if rgb_frame is None:
                print("[WARN] No RGB frame received.")
                time.sleep(args.delay)
                continue

            mask = predict_rgb_mask(model, rgb_frame, cfg, device, image_size)
            command = decide_navigation(mask)
            action = navigator.execute(command)

            if command == "STOP":
                robot.stop()

                elapsed_time = time.time() - run_start_time

                pose = robot.get_pose()

                if pose is not None:
                    x, y, th = pose
                    travelled_m = ((x ** 2 + y ** 2) ** 0.5) / 1000

                    print("\nGlass detected. Robot has stopped.")
                    print(f"Run time: {elapsed_time:.2f} seconds")
                    print(f"Travel distance: {travelled_m:.2f} metres")
                else:
                    print("\nGlass detected. Robot has stopped.")
                    print(f"Run time: {elapsed_time:.2f} seconds")

                break

            pose = robot.get_pose()
            if pose is not None:
                x, y, th = pose
                travelled_m = ((x ** 2 + y ** 2) ** 0.5) / 1000

                if travelled_m >=4:
                    robot.stop()

                    elapsed_time = time.time() - run_start_time

                    print("\nSafety stop activated.")
                    print(f"Run time: {elapsed_time:.2f} seconds")
                    print(f"Travel distance: {travelled_m:.2f} metres")

                    break
                print(f"Frame={frame_count} | Robot moving forward | Pose=({x:.1f}, {y:.1f}, {th:.1f})")
            else:
                print(f"Frame={frame_count} | Robot moving forward | Pose unavailable")

            frame_count += 1

            if args.max_frames > 0 and frame_count >= args.max_frames:
                break

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\nStopping system...")

    finally:
        robot.stop()
        camera.close()
        robot.close()
        print("System stopped safely.")


if __name__ == "__main__":
    main()