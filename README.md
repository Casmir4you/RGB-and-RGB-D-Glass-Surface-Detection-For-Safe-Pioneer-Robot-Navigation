# Comparative Evaluation of RGB and RGB-D Glass Surface Detection for Safe Pioneer Mobile Robot Navigation

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

**Author:** Ebubechukwu Amasiatu  
**Institution:** The University of Salford

## Overview

Glass surfaces remain difficult for autonomous mobile robots to detect because they often provide weak visual cues and unreliable depth measurements. This repository presents the implementation of an MSc research project comparing RGB-only and RGB-D semantic segmentation for glass surface detection using SegFormer.

Both models were trained, validated, and tested under identical experimental conditions using the RGB-D Glass Surface Detection dataset. The selected models were then integrated into a real-time perception framework for a Pioneer P3-DX mobile robot using Microsoft Kinect data.

The repository includes:

- RGB and RGB-D SegFormer implementations
- dataset preparation utilities
- training, validation, evaluation, and prediction pipelines
- quantitative and qualitative benchmark results
- Microsoft Kinect integration
- Pioneer P3-DX deployment software
- reproducible YAML experiment configurations

## Key Results

| Metric | RGB | RGB-D |
|---|---:|---:|
| Pixel Accuracy | **0.9429** | 0.9408 |
| Mean IoU | **0.8152** | 0.8085 |
| Glass IoU | **0.6961** | 0.6850 |
| Background IoU | **0.9344** | 0.9321 |
| Glass Precision | **0.8358** | 0.8333 |
| Glass Recall | **0.8063** | 0.7938 |
| Glass F1-score | **0.8208** | 0.8131 |

The RGB model achieved slightly higher held-out test performance across the reported metrics. Under the evaluated conditions, adding depth information did not improve test-set generalisation.

## Qualitative Comparison

![RGB and RGB-D qualitative comparison](results/comparison_panels/00000210_comparison%281%29.png)

The panel presents the original image, ground-truth mask, RGB prediction, and RGB-D prediction for a representative test sample.

## Real-Time Pioneer P3-DX Deployment

### RGB deployment

![Pioneer P3-DX RGB deployment](results/Representative%20Terminal%20Output%20of%20RGB%20Model%20Practical%20Deployment%20%281%29.png)

### RGB-D deployment

![Pioneer P3-DX RGB-D deployment](results/Representative%20Terminal%20Output%20of%20RGBD%20Model%20Practical%20Deployment%20%282%29.png)

The deployment outputs show live Microsoft Kinect input, robot movement, glass detection, controlled stopping, run time, travel distance, and safe system termination.

## Project Scope

This repository focuses on:

- glass surface perception
- binary semantic segmentation
- RGB versus RGB-D model comparison
- quantitative and qualitative evaluation
- real-time model deployment

It does not implement or evaluate a complete SLAM, path-planning, obstacle-avoidance, or autonomous decision-making stack.

## System Workflow

```text
RGB-D GSD Dataset
        │
        ▼
Dataset Preparation
        │
        ▼
 ┌───────────────┐
 │               │
 ▼               ▼
RGB Model     RGB-D Model
 │               │
 ▼               ▼
Training and Validation
        │
        ▼
Held-out Test Evaluation
        │
        ▼
Quantitative and Qualitative Comparison
        │
        ▼
Microsoft Kinect Deployment
        │
        ▼
Pioneer P3-DX Glass-Detection Response
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Casmir4you/RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation.git
cd RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Prepare the dataset

The RGB-D GSD dataset is not included because of its size. Use the utilities in `scripts/` and configure local dataset paths in:

```text
configs/rgb.yaml
configs/rgbd.yaml
```

### 5. Train the models

RGB:

```bash
bash scripts/train_rgb.sh
```

RGB-D:

```bash
bash scripts/train_rgbd.sh
```

Direct Python equivalents:

```bash
python -m src.train --config configs/rgb.yaml
python -m src.train --config configs/rgbd.yaml
```

### 6. Evaluate both models

```bash
bash scripts/evaluate.sh
```

## Repository Structure

```text
.
├── configs/
├── deployment/
├── outputs/
├── results/
│   ├── comparison_panels/
│   └── qualitative_analysis/
├── scripts/
├── src/
├── docs/
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore
```

A full directory description is available in [`docs/repository-structure.md`](docs/repository-structure.md).

## Documentation

- [Methodology and system architecture](docs/methodology.md)
- [Repository structure](docs/repository-structure.md)
- [Installation and environment setup](docs/installation.md)
- [Running the experiments](docs/experiments.md)
- [Deployment](docs/deployment.md)
- [Results and interpretation](docs/results.md)

## Core Contributions

1. A controlled comparison of RGB and RGB-D SegFormer models for glass surface segmentation.
2. A four-channel RGB-D adaptation of SegFormer.
3. A reproducible training and evaluation framework.
4. A real-time Kinect-based deployment pipeline for the Pioneer P3-DX.
5. Evidence that RGB-D input did not outperform RGB-only input on the held-out test set under the evaluated conditions.

## Citation

```bibtex
@misc{amasiatu2026glasssegmentation,
  author       = {Ebubechukwu Amasiatu},
  title        = {Comparative Evaluation of RGB and RGB-D Glass Surface Detection for Safe Pioneer Mobile Robot Navigation},
  year         = {2026},
  institution  = {The University of Salford},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/Casmir4you/RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation}},
  note         = {MSc Dissertation Repository}
}
```

## Acknowledgements

This project builds on open-source contributions from the SegFormer, Hugging Face Transformers, PyTorch, OpenCV, NumPy, Pandas, and wider computer-vision and robotic-perception communities. The author also acknowledges the creators of the RGB-D Glass Surface Detection dataset and the support of The University of Salford.

## Licence

This project is released under the MIT License. See [`LICENSE`](LICENSE).

## Contact

**Ebubechukwu Amasiatu**

- GitHub: https://github.com/Casmir4you
- Repository: https://github.com/Casmir4you/RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation

Issues, bug reports, and feature requests can be submitted through the repository's GitHub Issues page.
