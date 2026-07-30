# Repository Structure

## 1. Introduction

This document provides an overview of the organisation of the RGB and RGB-D Glass Surface Detection repository.

The repository has been designed to separate source code, configuration files, experimental outputs, documentation, and deployment utilities into clearly defined directories. This modular organisation improves readability, simplifies maintenance, and supports reproducible research by ensuring that each component of the project has a well-defined purpose.

Whether reproducing the benchmark experiments, reviewing the implementation, or deploying the trained models on the Pioneer P3-DX platform, understanding the repository structure enables users to quickly locate the files relevant to each stage of the workflow.

---

# 2. Repository Philosophy

The repository follows a modular design philosophy in which related functionality is grouped into dedicated directories.

Rather than combining training code, configuration files, documentation, and experimental results into a single location, each component is isolated according to its role within the project.

This organisation provides several advantages:

- improves code readability;
- simplifies debugging and maintenance;
- supports reproducibility;
- separates implementation from experimental results;
- keeps documentation independent of source code;
- enables future extensions without restructuring the project.

The repository has therefore been organised around the complete benchmark-to-robot workflow, beginning with dataset preparation and model training, progressing through benchmark evaluation, and concluding with practical robotic deployment.

---

# 3. Top-Level Directory Structure

The principal repository structure is shown below.

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
├── README.md
└── LICENSE
```

Each top-level directory has a specific responsibility within the project.

| Directory | Purpose |
|------------|---------|
| `configs/` | Experiment configuration files |
| `deployment/` | Robot deployment utilities |
| `docs/` | Project documentation |
| `outputs/` | Generated checkpoints and training outputs |
| `results/` | Evaluation results and visualisations |
| `scripts/` | Automation scripts |
| `src/` | Core implementation |
| `requirements.txt` | Python dependencies |
| `README.md` | Project overview |
| `LICENSE` | Repository licence |

Keeping these components separate reduces unnecessary coupling between different parts of the repository and makes it easier for researchers to focus on the specific area relevant to their work.

For example, users interested only in reproducing the benchmark experiments primarily interact with the `configs/`, `scripts/`, `src/`, and `results/` directories, while users deploying the trained models on a Pioneer P3-DX platform additionally make use of the `deployment/` directory.

---

# 4. Source Code (`src/`)

The `src/` directory contains the core implementation of the project. All primary functionality related to dataset processing, model construction, training, evaluation, and utility functions is implemented within this directory.

Rather than placing all Python files in a single location, the repository organises related components into logical modules. This modular structure improves maintainability, simplifies debugging, and allows individual components to be updated without affecting unrelated parts of the codebase.

A typical structure is shown below.

```text
src/
├── datasets/
├── models/
├── utils/
├── train.py
└── evaluate.py
```

Each component has a specific responsibility.

| Component | Purpose |
|-----------|---------|
| `datasets/` | Dataset loading and preprocessing |
| `models/` | Model architecture definitions |
| `utils/` | Shared helper functions |
| `train.py` | Model training pipeline |
| `evaluate.py` | Benchmark evaluation pipeline |

During a typical experiment, `train.py` coordinates the overall training process by loading the configuration, constructing the dataset, creating the selected model, performing optimisation, validating performance, and saving the best-performing checkpoint.

Once training has completed, `evaluate.py` loads the selected checkpoint and computes the benchmark metrics reported throughout the project.

---

# 5. Configuration Files (`configs/`)

The `configs/` directory contains the YAML configuration files that define each benchmark experiment.

Separating configuration from source code allows experiments to be reproduced or modified without changing the implementation itself. Users can adjust experimental settings by editing the configuration files rather than modifying Python scripts.

The repository includes separate configuration files for each benchmark model.

```text
configs/
├── rgb.yaml
└── rgbd.yaml
```

These files specify important experimental parameters, including:

- dataset locations;
- model configuration;
- optimisation settings;
- training hyperparameters;
- output directories;
- checkpoint behaviour.

Using configuration files also helps maintain consistency between experiments by ensuring that all settings are stored in a single location.

---

# 6. Scripts (`scripts/`)

The `scripts/` directory contains automation utilities that simplify common tasks performed throughout the project.

Instead of requiring users to manually execute long Python commands, the repository provides scripts that launch predefined workflows for training, evaluation, and qualitative analysis.

Typical scripts include:

```text
scripts/
├── train_rgb.sh
├── train_rgbd.sh
├── evaluate.sh
└── make_comparison_panels.py
```

These scripts provide several advantages:

- reduce typing errors;
- ensure experiments are executed consistently;
- simplify reproduction of published results;
- provide a standard entry point for common workflows.

Researchers new to the repository are encouraged to use these scripts rather than invoking individual Python modules directly.

---

# 7. Results (`results/`)

The `results/` directory stores the outputs generated during benchmark evaluation.

Unlike the `outputs/` directory, which primarily contains intermediate training artefacts, the `results/` directory focuses on materials used to analyse and interpret model performance.

Typical contents include:

```text
results/
├── comparison_panels/
├── qualitative_analysis/
├── experiment_summary.csv
└── final_model_summary.txt
```

The generated artefacts include:

- benchmark performance summaries;
- qualitative segmentation visualisations;
- comparison panels;
- consolidated experiment metrics.

These files provide the evidence used to compare the RGB and early-fusion RGB-D models and support the conclusions presented in the accompanying research paper.

---

# 8. Outputs (`outputs/`)

The `outputs/` directory contains the artefacts produced during model training.

Typical contents include:

```text
outputs/
├── RGB/
│   ├── checkpoints/
│   ├── logs/
│   └── predictions/
│
└── RGBD/
    ├── checkpoints/
    ├── logs/
    └── predictions/
```

Each experiment generates its own collection of outputs, allowing multiple training runs to be stored independently.

Common artefacts include:

- model checkpoints;
- training logs;
- validation histories;
- prediction outputs;
- intermediate experiment files.

Separating training outputs from benchmark results helps maintain a clear distinction between model development and final experimental analysis.

The checkpoint selected from this directory is subsequently used during held-out benchmark evaluation and, where applicable, practical deployment on the Pioneer P3-DX mobile robot.

---

# 9. Documentation (`docs/`)

The `docs/` directory contains the supporting documentation for the repository.

Rather than embedding lengthy explanations within the source code, the project documentation is organised into dedicated Markdown files that describe the methodology, experiments, deployment process, results, installation, and repository organisation.

A typical structure is shown below.

```text
docs/
├── methodology.md
├── experiments.md
├── deployment.md
├── results.md
├── installation.md
└── repository-structure.md
```

Each document focuses on a specific aspect of the project.

| Document | Purpose |
|----------|---------|
| `methodology.md` | Experimental design and implementation methodology |
| `experiments.md` | Benchmark and deployment procedures |
| `deployment.md` | Real-world robot deployment workflow |
| `results.md` | Quantitative and qualitative evaluation |
| `installation.md` | Environment setup and dependency installation |
| `repository-structure.md` | Repository organisation and architecture |

Separating documentation into focused guides improves readability and allows users to locate relevant information without navigating through lengthy monolithic documents.

---

# 10. Deployment (`deployment/`)

The `deployment/` directory contains the components required to integrate the trained segmentation models with the Pioneer P3-DX mobile robot.

Unlike the benchmark experiments, which operate on a static dataset, the deployment workflow processes live sensor data acquired from the robot's onboard camera system.

A typical deployment structure is shown below.

```text
deployment/
├── camera/
├── inference/
├── navigation/
└── utilities/
```

The deployment components work together to perform the following tasks:

- acquire live RGB or RGB-D images;
- preprocess sensor data;
- execute semantic segmentation;
- analyse the generated segmentation masks;
- apply the center-ratio decision rule;
- communicate navigation commands to the robot.

Researchers interested only in reproducing the benchmark experiments do not need to interact with this directory. However, it becomes essential when extending the project from offline evaluation to real-time robotic operation.

---

# 11. Repository Workflow

Although the repository is divided into multiple directories, each component contributes to a single benchmark-to-robot workflow.

The overall architecture is illustrated below.

```text
Dataset
    │
    ▼
Configuration Files
    │
    ▼
Training Pipeline (src/)
    │
    ▼
Model Checkpoints (outputs/)
    │
    ▼
Benchmark Evaluation (results/)
    │
    ▼
Qualitative Analysis
    │
    ▼
Robot Deployment (deployment/)
```

Each stage builds upon the outputs generated by the previous stage.

For example:

- configuration files define the experimental settings;
- the source code executes training and evaluation;
- checkpoints produced during training are stored in the `outputs/` directory;
- benchmark metrics and visualisations are written to the `results/` directory;
- the selected checkpoint is then used during practical deployment on the Pioneer P3-DX.

This structured workflow helps ensure that experiments remain reproducible and that benchmark and deployment results are derived from the same trained models.

---

# 12. Repository Summary

This repository has been organised to support the complete lifecycle of a semantic segmentation research project, from environment setup and model development through benchmark evaluation and practical robotic deployment.

Each top-level directory has a clearly defined purpose:

- `src/` implements the core functionality;
- `configs/` defines the experimental settings;
- `scripts/` automates common workflows;
- `outputs/` stores training artefacts;
- `results/` contains benchmark results and visualisations;
- `deployment/` enables real-world robot integration;
- `docs/` provides comprehensive project documentation.

By separating these responsibilities into dedicated modules, the repository remains organised, maintainable, and easy to navigate. This structure supports reproducible research, simplifies future development, and provides a clear framework for extending the project to new datasets, model architectures, or robotic platforms.

Together with the accompanying documentation, the repository provides a complete reference implementation of the benchmark-to-robot evaluation framework developed in this project.