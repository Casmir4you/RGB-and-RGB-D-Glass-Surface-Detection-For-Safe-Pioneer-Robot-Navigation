# Installation and Environment Setup

## 1. Introduction

This document provides step-by-step instructions for setting up the software environment required to reproduce the experiments presented in this repository. The installation process includes preparing the Python environment, installing all required dependencies, configuring the RGB-D Glass Surface Detection (RGB-D GSD) dataset, and verifying that the system is ready for training, evaluation, and practical deployment.

The repository has been developed using Python 3.11 together with PyTorch and the Hugging Face Transformers library. Although training can be performed on a CPU, a CUDA-compatible NVIDIA GPU is strongly recommended to achieve practical training times.

Following the installation procedure described in this guide ensures that the repository environment is consistent with that used during the benchmark and deployment experiments.

---

# 2. System Requirements

The repository has been tested using a modern Windows development environment.

The minimum recommended system specification is:

| Component | Recommendation |
|------------|---------------|
| Operating System | Windows 10/11 (64-bit) |
| Python | 3.11 |
| RAM | 16 GB minimum |
| Storage | 20 GB available |
| GPU | NVIDIA CUDA-compatible GPU (recommended) |

Linux and macOS are also supported provided that the required Python dependencies and compatible versions of PyTorch are installed.

Although CPU-only execution is possible, training transformer-based semantic segmentation models without GPU acceleration may require substantially longer execution times.

---

# 3. Hardware Requirements

Different stages of the project require different hardware capabilities.

### Benchmark Training

Recommended hardware:

- NVIDIA CUDA-compatible GPU
- 16 GB system memory
- Multi-core processor
- SSD storage

### Benchmark Evaluation

Benchmark evaluation may be performed using either a GPU or CPU, although GPU inference significantly reduces evaluation time.

### Practical Deployment

Practical deployment additionally requires:

- Pioneer P3-DX mobile robot
- Microsoft Kinect for Windows (First Generation)
- Compatible deployment laptop
- NVIDIA GPU for real-time inference

Researchers interested only in reproducing the benchmark experiments do not require the deployment hardware.

---

# 4. Software Requirements

The repository depends on the following principal software packages.

| Component | Version |
|------------|---------|
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

These dependencies are installed automatically through the repository requirements file.

Users are encouraged to install the latest compatible CUDA-enabled version of PyTorch appropriate for their operating system and NVIDIA driver configuration.

---

# 5. Clone the Repository

The first step is to obtain a local copy of the project repository from GitHub.

Clone the repository using Git:

```bash
git clone https://github.com/Casmir4you/RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation.git
```

Navigate into the project directory:

```bash
cd RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation
```

Once cloned successfully, the project directory will contain the source code, configuration files, documentation, scripts, deployment utilities, and supporting resources required for reproducing the experiments.

Before continuing, confirm that the repository structure matches the documentation provided in `docs/repository-structure.md`.

---

# 6. Create a Python Virtual Environment

Creating a dedicated Python virtual environment is strongly recommended.

Using a virtual environment isolates the project dependencies from other Python installations on the system and helps prevent package version conflicts.

## Windows

Create the virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

---

## Linux and macOS

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

---

Once activated, the command prompt should indicate that the virtual environment is active.

For example:

```text
(.venv) C:\Projects\RGB-and-RGB-D-Glass-Surface-Detection>
```

All remaining installation commands should be executed within this environment.

---

# 7. Install Project Dependencies

After activating the virtual environment, upgrade `pip` to the latest version.

```bash
pip install --upgrade pip
```

Next, install all required project dependencies.

```bash
pip install -r requirements.txt
```

The requirements file installs the complete software environment used throughout the project, including:

- PyTorch
- TorchVision
- Hugging Face Transformers
- Accelerate
- OpenCV
- NumPy
- Pillow
- Pandas
- PyYAML
- Scikit-learn
- TQDM

Depending on the internet connection and hardware configuration, installation may require several minutes.

If installation completes successfully, the repository is ready for dataset configuration and experiment setup. :contentReference[oaicite:1]{index=1}

---

# 8. Verify the Installation

Before downloading the dataset or beginning model training, verify that the software environment has been installed correctly.

Create a Python interpreter and execute:

```python
import torch

print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
```

A successful installation should display output similar to:

```text
PyTorch: 2.x.x
CUDA available: True
```

If `CUDA available` returns `True`, PyTorch has successfully detected a compatible NVIDIA GPU and training can utilise hardware acceleration.

If the result is:

```text
CUDA available: False
```

training will still function, but all computations will be performed on the CPU, resulting in significantly longer training times.

---

## Verify the Repository Structure

Before continuing, confirm that the repository contains the expected directories.

A correctly installed repository should resemble:

```text
RGB-and-RGB-D-Glass-Surface-Detection-For-Safe-Pioneer-Robot-Navigation/

├── configs/
├── deployment/
├── docs/
├── outputs/
├── results/
├── scripts/
├── src/
├── requirements.txt
└── README.md
```

If any major directories are missing, the repository may not have cloned correctly.

---

## Installation Checklist

Before proceeding to dataset preparation, verify that the following tasks have been completed.

| Task | Status |
|-------|--------|
| Repository cloned | ✓ |
| Virtual environment created | ✓ |
| Virtual environment activated | ✓ |
| Dependencies installed | ✓ |
| PyTorch imports successfully | ✓ |
| CUDA detected (recommended) | ✓ |
| Repository structure verified | ✓ |

Once every item has been completed successfully, the software environment is ready for dataset configuration and experiment execution. :contentReference[oaicite:2]{index=2}

---

# 9. Dataset Preparation

Before any training or evaluation experiments can be performed, the RGB-D Glass Surface Detection (RGB-D GSD) dataset must be downloaded and organised according to the directory structure expected by the repository.

The dataset should be extracted into the designated data directory while preserving the original folder hierarchy. Any associated manifest files or train, validation, and test splits should remain unchanged to ensure consistency with the experimental methodology.

A typical dataset directory structure is shown below.

```text
data/
└── RGBD-GSD/
    ├── train/
    │   ├── rgb/
    │   ├── depth/
    │   └── masks/
    ├── val/
    │   ├── rgb/
    │   ├── depth/
    │   └── masks/
    └── test/
        ├── rgb/
        ├── depth/
        └── masks/
```

After copying the dataset into the appropriate location, confirm that all image, depth, and segmentation mask files are present before proceeding.

If the dataset is incomplete or incorrectly organised, training and evaluation scripts may fail to locate the required files.

---

# 10. Configuration Files

The repository uses YAML configuration files to define the parameters for each experiment.

The primary configuration files are located in the `configs/` directory.

```text
configs/
├── rgb.yaml
└── rgbd.yaml
```

These configuration files specify settings such as:

- dataset location;
- training parameters;
- model configuration;
- optimisation settings;
- output directories.

Before running any experiments, review the dataset paths specified within the configuration files and update them if your local dataset is stored in a different location.

Maintaining accurate configuration files helps ensure that all scripts execute successfully without requiring modifications to the source code.

---

# 11. Verify the Dataset

Once the dataset has been prepared and the configuration files have been updated, verify that the repository can successfully access the data.

A successful verification should confirm that:

- the training dataset loads correctly;
- the validation dataset loads correctly;
- the test dataset loads correctly;
- RGB images can be paired with their corresponding depth images;
- segmentation masks are correctly associated with each image pair.

If the dataset loads without errors, the installation process is complete and the repository is ready for experimentation.

Any file-not-found or indexing errors should be resolved before beginning model training.

---

# 12. Common Installation Problems

Although the installation process is straightforward, several common issues may prevent the repository from running correctly.

## Python Version

Ensure that Python 3.11 (or another supported version specified by the repository) is being used.

You can verify the installed version with:

```bash
python --version
```

---

## Missing Dependencies

If a module cannot be imported, reinstall the project dependencies.

```bash
pip install -r requirements.txt
```

If necessary, upgrade `pip` before reinstalling.

---

## Incorrect Dataset Paths

If training or evaluation scripts report that dataset files cannot be found, verify that:

- the dataset has been extracted correctly;
- the directory structure matches the expected layout;
- the paths defined in the configuration files are correct.

---

## CUDA Not Detected

If PyTorch reports that CUDA is unavailable despite having a compatible NVIDIA GPU, verify that:

- the latest NVIDIA drivers are installed;
- the appropriate CUDA-enabled version of PyTorch has been installed;
- the GPU is recognised by the operating system.

Users without GPU support can still execute the repository using CPU-based training, although training and inference will require substantially more time.

---

## Interrupted Installation

If package installation is interrupted, reactivate the virtual environment and rerun the dependency installation command.

```bash
pip install -r requirements.txt
```

Most package installation issues can be resolved by repeating the installation after restoring a stable internet connection.

---

# 13. Performance Recommendations

For the best training and evaluation experience, the following practices are recommended.

- Use an NVIDIA GPU with CUDA support whenever possible.
- Store the dataset on an SSD to reduce loading times.
- Close unnecessary applications during model training to maximise available system memory.
- Ensure sufficient disk space is available for checkpoints, logs, and generated results.
- Keep the Python environment dedicated to this project to avoid dependency conflicts.

These recommendations help improve training efficiency and minimise unexpected runtime issues.

---

# 14. Next Steps

After completing the installation and verifying the dataset, the repository is ready for experimentation.

The recommended workflow is:

1. Review the experimental methodology in `docs/methodology.md`.
2. Follow the benchmark procedures described in `docs/experiments.md`.
3. Analyse the quantitative and qualitative outcomes presented in `docs/results.md`.
4. If the required hardware is available, proceed with the deployment workflow described in `docs/deployment.md`.

Following this sequence provides a structured path from environment setup through benchmark evaluation and, ultimately, practical robotic deployment.

The installation process is now complete, and the repository is fully prepared for reproducing the benchmark-to-robot evaluation presented in the accompanying research paper.