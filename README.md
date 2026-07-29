# RGB and RGB-D Glass Surface Detection for Safe Pioneer Robot Navigation

## Overview

This repository contains the official implementation and reproducibility package for the comparative evaluation of RGB and RGB-D glass surface detection methods for safe mobile robot navigation.

The project investigates whether incorporating depth information improves the detection of transparent glass surfaces compared to conventional RGB imaging. Two SegFormer semantic segmentation models were developed and evaluated using RGB and RGB-D data before being deployed on a Pioneer P3-DX mobile robot for real-world validation.

The primary objective is to improve navigation safety by enabling the robot to detect glass obstacles and stop before collision.

---

## Features

- RGB glass surface detection using SegFormer
- RGB-D glass surface detection using SegFormer
- Comparative evaluation of RGB and RGB-D approaches
- Training and evaluation pipeline
- Real-time deployment on Pioneer P3-DX mobile robot
- Kinect RGB-D camera integration
- Real-time semantic segmentation
- Glass-aware robot safety stopping
- Reproducible experiments

---

## Research Objectives

The objectives of this work are to:

- Develop an RGB-based glass surface detection model.
- Develop an RGB-D glass surface detection model.
- Compare the detection performance of both approaches.
- Evaluate real-time deployment on a Pioneer P3-DX mobile robot.
- Investigate whether depth information improves safe robot navigation around transparent obstacles.

---

## Repository Structure

```
project/
│
├── configs/                 # Training configurations
├── datasets/                # Dataset utilities
├── deployment/              # Real-time deployment
│   ├── deploy_rgb.py
│   ├── deploy_rgbd.py
│   ├── main_rgb.py
│   ├── main_rgbd.py
│   ├── navigation.py
│   ├── robot_controller.py
│   └── kinect_capture.py
│
├── models/                  # Trained model checkpoints
├── outputs/                 # Training outputs
├── src/                     # Source code
├── results/                 # Evaluation results
└── README.md
```

---

## Dataset

The models were trained and evaluated using the RGB-D Glass Surface Detection (RGB-D GSD) dataset.

Dataset characteristics include:

- RGB images
- Registered depth images
- Binary segmentation masks
- Transparent glass surfaces
- Indoor scenes

---

## Model Architecture

Both approaches use the SegFormer semantic segmentation architecture.

### RGB Model

- Input: RGB image
- Backbone: MiT-B0
- Output: Binary glass segmentation mask

### RGB-D Model

- Input: RGB + Depth
- Backbone: Modified MiT-B0 (4-channel input)
- Output: Binary glass segmentation mask

---

## Hardware

### Training

- NVIDIA GeForce RTX 4050 Laptop GPU
- CUDA
- PyTorch

### Deployment

- Pioneer P3-DX Mobile Robot
- Microsoft Kinect RGB-D Camera
- Python
- MobileSim / Physical Pioneer Robot

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Training

Train the RGB model

```bash
python src/train.py --config configs/rgb.yaml
```

Train the RGB-D model

```bash
python src/train.py --config configs/rgbd.yaml
```

---

## Evaluation

Evaluate the trained models

```bash
python src/evaluate.py
```

Performance metrics include:

- Mean IoU
- Pixel Accuracy
- Precision
- Recall
- F1-score
- Per-class IoU

---

## Deployment

Real-time deployment is provided for both RGB and RGB-D systems.

RGB deployment

```bash
python deployment/main_rgb.py
```

RGB-D deployment

```bash
python deployment/main_rgbd.py
```

The deployment pipeline consists of:

1. Kinect image acquisition
2. Image preprocessing
3. SegFormer inference
4. Glass segmentation
5. Navigation decision
6. Pioneer robot control

The robot moves forward until glass is detected or the predefined safety distance is reached, after which it stops.

---

## Experimental Evaluation

The repository includes:

- Offline semantic segmentation evaluation
- RGB versus RGB-D comparison
- Real-world deployment experiments
- Robot safety stopping validation
- Inference time analysis
- Frame rate evaluation

---

## Citation

If you use this work in your research, please cite:

```text


## License

This project is released under the MIT License.

---

## Acknowledgements

This work was completed as part of the MSc Robotics and Automation programme at the University of Salford.

The author gratefully acknowledges the support of the supervisors, the Robotics Laboratory, and the developers of:

- SegFormer
- PyTorch
- Hugging Face Transformers
- RGB-D Glass Surface Detection Dataset
- Pioneer P3-DX Mobile Robot Platform

---

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue or contact the repository owner.
