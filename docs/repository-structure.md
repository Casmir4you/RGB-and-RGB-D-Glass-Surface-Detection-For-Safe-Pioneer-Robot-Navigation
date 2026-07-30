# Repository Structure

```text
RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation
│
├── configs/
│   ├── rgb.yaml
│   └── rgbd.yaml
│
├── deployment/
│   ├── kinect_bridge/
│   │   ├── KinectBridge.cs
│   │   └── KinectBridge.exe
│   ├── models/
│   │   ├── rgb_best_model.pt
│   │   ├── rgbd_best_model.pt
│   │   ├── rgb_config.yaml
│   │   └── rgbd_config.yaml
│   ├── kinect_capture.py
│   ├── navigation.py
│   ├── pioneer_rgb_deployment.py
│   ├── pioneer_rgbd_deployment.py
│   ├── rgb_inference.py
│   ├── rgbd_inference.py
│   └── robot_controller.py
│
├── outputs/
│   ├── RGB/
│   │   ├── config_used.json
│   │   ├── history.json
│   │   └── test_metrics.json
│   └── RGBD/
│       ├── config_used.json
│       ├── history.json
│       └── test_metrics.json
│
├── results/
│   ├── comparison_panels/
│   │   └── 00000210_comparison(1).png
│   ├── qualitative_analysis/
│   │   ├── rgb/
│   │   │   └── 00000008_rgb_overlay.png
│   │   └── rgbd/
│   │       └── 00000008_rgbd_overlay.png
│   ├── experiment_summary.csv
│   ├── final_model_summary.txt
│   ├── Representative Terminal Output of RGB Model Practical Deployment (1).png
│   └── Representative Terminal Output of RGBD Model Practical Deployment (2).png
│
├── scripts/
│   ├── download_rgbd_gsd.py
│   ├── evaluate.sh
│   ├── export_rgbd_gsd.py
│   ├── inspect_dataset.py
│   ├── inspect_depth_channel.py
│   ├── make_comparison_panels.py
│   ├── test_loader.py
│   ├── train_rgb.sh
│   └── train_rgbd.sh
│
├── src/
│   ├── datasets/
│   ├── models/
│   ├── utils/
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── docs/
│   ├── methodology.md
│   ├── repository-structure.md
│   ├── installation.md
│   ├── experiments.md
│   ├── deployment.md
│   └── results.md
│
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore
```

## Directory Descriptions

### `configs/`

Contains the YAML configuration files for the RGB and RGB-D experiments.

### `deployment/`

Contains Kinect acquisition, model inference, robot control, navigation integration, and the main RGB and RGB-D deployment applications.

The models in `deployment/models/` are the benchmark-selected models retained for deployment.

### `outputs/`

Contains configuration snapshots, training histories, and held-out test metrics for both experiments.

Temporary and duplicate checkpoints are excluded to reduce repository size.

### `results/`

Contains the quantitative summaries, qualitative outputs, comparison panels, and representative live deployment screenshots already produced by the project.

### `scripts/`

Contains dataset download, export, inspection, training, evaluation, loader-testing, and comparison-panel scripts.

### `src/`

Contains the core machine-learning implementation:

- dataset loaders
- model definitions
- utilities
- training
- evaluation
- prediction

### `docs/`

Contains detailed public documentation while keeping the main README concise.
