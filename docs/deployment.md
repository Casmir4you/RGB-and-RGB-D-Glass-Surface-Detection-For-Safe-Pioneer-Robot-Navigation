# Pioneer P3-DX Deployment

## Hardware and Software Context

The deployment framework was developed for:

- Pioneer P3-DX mobile robot
- Microsoft Kinect RGB-D sensor
- Windows-based Kinect bridge
- Python inference and robot-integration modules

## Deployment Components

| File | Purpose |
|---|---|
| `deployment/kinect_capture.py` | Captures RGB and depth frames |
| `deployment/rgb_inference.py` | Performs RGB segmentation inference |
| `deployment/rgbd_inference.py` | Performs RGB-D segmentation inference |
| `deployment/robot_controller.py` | Interfaces with the Pioneer P3-DX |
| `deployment/navigation.py` | Connects perception output with the navigation response |
| `deployment/pioneer_rgb_deployment.py` | Main RGB deployment application |
| `deployment/pioneer_rgbd_deployment.py` | Main RGB-D deployment application |

## Deployment Models

```text
deployment/models/rgb_best_model.pt
deployment/models/rgbd_best_model.pt
```

These are the selected models retained for practical deployment.

## Deployment Workflow

1. Start the Kinect bridge.
2. Confirm that RGB and depth data are being received.
3. Load the required deployment configuration and model.
4. Start either the RGB or RGB-D deployment application.
5. Confirm that segmentation masks are being produced.
6. Confirm communication with the Pioneer P3-DX.
7. Test movement and stopping in a controlled environment.

## Representative RGB Run

![Pioneer P3-DX RGB deployment](../results/Representative%20Terminal%20Output%20of%20RGB%20Model%20Practical%20Deployment%20%281%29.png)

The displayed run shows continuous robot movement followed by glass detection, robot stopping, recorded run time, travel distance, and safe system termination.

## Representative RGB-D Run

![Pioneer P3-DX RGB-D deployment](../results/Representative%20Terminal%20Output%20of%20RGBD%20Model%20Practical%20Deployment%20%282%29.png)

The displayed run shows live RGB-D acquisition, robot movement, glass detection, stopping, and safe termination. The terminal also records an intermittent depth-frame permission warning during the run.

## Scope Note

The deployment software provides the glass-perception component and robot response interface. It does not constitute a fully evaluated autonomous navigation stack.
