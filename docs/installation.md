# Installation and Environment Setup

## Software Environment

| Component | Version |
|---|---|
| Python | 3.11 |
| PyTorch | 2.1 or later |
| TorchVision | 0.16 or later |
| Hugging Face Transformers | 4.40 or later |
| Accelerate | 0.29 or later |
| OpenCV | 4.8 or later |
| NumPy | 1.24 or later |
| Pillow | 10.0 or later |
| PyYAML | 6.0 or later |
| Pandas | 2.0 or later |
| TQDM | 4.66 or later |
| Scikit-learn | 1.3 or later |

A CUDA-compatible NVIDIA GPU is strongly recommended for training.

## Clone the Repository

```bash
git clone https://github.com/Casmir4you/RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation.git
cd RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation
```

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Dataset Preparation

The RGB-D Glass Surface Detection dataset is not included because of its size.

The following utilities are provided:

```text
scripts/download_rgbd_gsd.py
scripts/export_rgbd_gsd.py
scripts/inspect_dataset.py
scripts/inspect_depth_channel.py
scripts/test_loader.py
```

Configure the local dataset paths in:

```text
configs/rgb.yaml
configs/rgbd.yaml
```

The dataset structure must match the paths and manifest logic expected by the repository's configuration files and dataset loader.

## Verify the Environment

```python
import torch

print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
```

## Common Problems

### Dataset not found

Check the local paths in `configs/rgb.yaml` and `configs/rgbd.yaml`.

### Missing dependency

```bash
pip install -r requirements.txt
```

### CUDA not available

Confirm that the installed PyTorch build, NVIDIA driver, and CUDA runtime are mutually compatible.

### Shell scripts do not run on Windows

Use Git Bash or run the Python modules directly:

```bash
python -m src.train --config configs/rgb.yaml
python -m src.train --config configs/rgbd.yaml
```
