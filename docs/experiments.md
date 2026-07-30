# Running the Experiments

## 1. Introduction

This document describes the complete experimental workflow used to evaluate RGB and early-fusion RGB-D semantic segmentation models for transparent glass detection. It provides the sequence of experiments required to reproduce the benchmark evaluation, generate qualitative visualisations, and perform practical deployment using the Pioneer P3-DX mobile robot.

The experiments are organised according to the benchmark-to-robot evaluation methodology adopted throughout this project. The workflow begins with controlled benchmark training and evaluation before progressing to qualitative analysis and practical robot deployment.

Following the documented sequence ensures that every experiment is performed under consistent conditions, allowing meaningful comparison between the RGB and RGB-D models.

---

# 2. Experimental Philosophy

The experiments were designed as a controlled comparative study in which the RGB and early-fusion RGB-D models differ only in their input modality.

To ensure a fair comparison:

- both models use the same SegFormer-B0 architecture;
- both are trained using the same dataset;
- both use identical optimisation settings;
- both follow the same training, validation, and testing procedures;
- both are evaluated using identical benchmark metrics;
- both are deployed using the same robotic platform and decision logic.

Maintaining identical experimental conditions ensures that observed differences arise from the additional depth modality rather than unrelated implementation differences.

The experimental workflow therefore supports direct comparison between RGB perception and early-fusion RGB-D perception under controlled conditions.

---

# 3. Experiment Overview

The complete workflow consists of six principal stages.

```text
Dataset Preparation
          │
          ▼
Train RGB Model
          │
          ▼
Train RGB-D Model
          │
          ▼
Benchmark Evaluation
          │
          ▼
Generate Qualitative Results
          │
          ▼
Deploy on Pioneer P3-DX
```

Each stage builds upon the previous one.

Training produces the model checkpoints, benchmark evaluation measures quantitative performance, qualitative analysis provides visual evidence of segmentation quality, and practical deployment evaluates semantic perception during real robot operation.

---

# 4. Prerequisites

Before running the experiments, ensure that the following requirements have been completed:

- the repository has been cloned;
- all required Python packages have been installed;
- the RGB-D GSD dataset has been downloaded and prepared;
- dataset paths have been configured correctly;
- CUDA is available (recommended for training);
- the required configuration files are present.

The benchmark experiments require the configuration files:

```text
configs/rgb.yaml
configs/rgbd.yaml
```

Training should only begin after the dataset loader has been verified successfully.

For practical deployment, additional hardware is required:

- Pioneer P3-DX mobile robot;
- Microsoft Kinect for Windows (first generation);
- deployment laptop with a compatible NVIDIA GPU.

Users interested only in reproducing the benchmark experiments may omit the deployment stage.

---

# 5. RGB Benchmark Experiment

The first experiment establishes the RGB-only baseline for transparent glass segmentation.

This experiment trains a standard SegFormer-B0 model using only the three-channel RGB images from the RGB-D Glass Surface Detection (RGB-D GSD) dataset. The resulting model serves as the benchmark against which the early-fusion RGB-D model is compared throughout this project.

All training parameters—including optimisation settings, learning rate schedule, loss function, and checkpoint selection—remain identical to those used for the RGB-D experiment. Consequently, the only experimental difference between the two models is the input modality.

The RGB benchmark experiment is executed using either the provided shell script or the equivalent Python command.

### Shell Script

```bash
bash scripts/train_rgb.sh
```

### Equivalent Python Command

```bash
python -m src.train --config configs/rgb.yaml
```

During training, the experiment automatically:

- loads the RGB training dataset;
- trains the SegFormer-B0 network;
- evaluates performance on the validation set after each epoch;
- saves the checkpoint achieving the highest validation Mean IoU;
- records the complete training history.

The selected checkpoint is subsequently used for benchmark testing and practical deployment. :contentReference[oaicite:1]{index=1}

---

# 6. RGB-D Benchmark Experiment

The second benchmark experiment evaluates the proposed early-fusion RGB-D architecture.

Unlike the RGB baseline, this experiment combines aligned RGB and depth images into a four-channel input tensor before inference. The first convolutional projection layer of the SegFormer-B0 encoder is expanded to accept the additional depth channel while preserving the pretrained RGB weights.

Aside from this architectural modification, every aspect of training remains identical to the RGB experiment.

The RGB-D benchmark experiment is executed using:

### Shell Script

```bash
bash scripts/train_rgbd.sh
```

### Equivalent Python Command

```bash
python -m src.train --config configs/rgbd.yaml
```

The experiment performs the same sequence of operations as the RGB benchmark:

- dataset loading;
- model training;
- validation after each epoch;
- automatic checkpoint selection;
- training history recording.

Maintaining identical experimental conditions ensures that any performance differences observed between the two models can be attributed to the inclusion of depth information rather than differences in optimisation or training strategy. :contentReference[oaicite:2]{index=2}

---

# 7. Training Procedure

Both benchmark experiments follow the same training workflow.

```text
Load Configuration
        │
        ▼
Load Dataset
        │
        ▼
Create SegFormer Model
        │
        ▼
Training Loop
        │
        ▼
Validation
        │
        ▼
Checkpoint Selection
        │
        ▼
Save Results
```

During each epoch, the model processes batches from the training dataset and updates the network parameters using the configured optimisation strategy.

At the end of every epoch, the model is evaluated on the validation dataset. The validation Mean Intersection over Union (mIoU) is used to determine whether the current model represents the best-performing checkpoint.

If validation performance improves, the checkpoint is saved automatically.

Training continues until either:

- the maximum number of epochs is reached; or
- early stopping criteria are satisfied.

This procedure ensures that the benchmark evaluation is performed using the strongest available model rather than simply the final training epoch.

---

# 8. Validation Procedure

Validation is performed throughout training to monitor model performance and guide checkpoint selection.

Unlike the held-out test dataset, the validation dataset is used exclusively during model development.

Its primary purposes are to:

- monitor learning progress;
- detect performance improvements;
- identify overfitting;
- select the best-performing checkpoint.

The benchmark evaluation therefore consists of three independent stages:

```text
Training Dataset
        │
        ▼
Parameter Learning

Validation Dataset
        │
        ▼
Model Selection

Held-Out Test Dataset
        │
        ▼
Final Performance Evaluation
```

Separating training, validation, and testing ensures that the final benchmark metrics provide an unbiased assessment of model performance on previously unseen data.

Only the checkpoint selected using validation performance proceeds to the held-out benchmark evaluation and the subsequent practical deployment experiments.

---

# 9. Held-Out Test Evaluation

Following completion of training and validation, the selected checkpoint for each model is evaluated on the held-out test partition of the RGB-D Glass Surface Detection (RGB-D GSD) dataset.

Unlike the validation dataset, the test dataset is not used during model development or checkpoint selection. It provides an independent assessment of model performance on previously unseen images and serves as the basis for the benchmark results reported throughout this project.

The benchmark evaluation is executed using the supplied evaluation script.

### Shell Script

```bash
bash scripts/evaluate.sh
```

The evaluation script automatically:

- loads the selected RGB checkpoint;
- loads the selected RGB-D checkpoint;
- evaluates each model on the held-out test dataset;
- computes all benchmark metrics;
- stores the quantitative results for subsequent analysis.

The evaluation process produces the benchmark metrics used throughout the accompanying research paper, including:

- Pixel Accuracy;
- Mean Intersection over Union (mIoU);
- Glass IoU;
- Background IoU;
- Glass Precision;
- Glass Recall;
- Glass F1-score.

Using a common evaluation procedure for both models ensures that the reported benchmark results remain directly comparable. :contentReference[oaicite:1]{index=1}

---

# 10. Qualitative Comparison Panel Generation

Numerical metrics provide an objective measure of segmentation performance, but visual inspection remains an important component of semantic segmentation evaluation.

To support qualitative analysis, the repository includes a utility that generates comparison panels for representative test images.

### Command

```bash
python scripts/make_comparison_panels.py
```

The generated comparison panels are saved to:

```text
results/comparison_panels/
```

Each comparison panel contains four corresponding views:

1. Original RGB image.
2. Ground-truth segmentation mask.
3. RGB model prediction.
4. RGB-D model prediction.

Displaying these outputs side by side allows direct visual comparison of segmentation quality between the two models and helps identify differences in localisation accuracy, object boundaries, and prediction completeness.

The comparison panels complement the quantitative benchmark metrics by providing interpretable visual evidence of model behaviour. :contentReference[oaicite:2]{index=2}

---

# 11. Practical Robot Deployment

After benchmark evaluation has been completed, the selected checkpoints can be deployed on the Pioneer P3-DX mobile robot for real-time semantic glass detection.

Deployment uses the same benchmark-selected models without additional training or fine-tuning.

The deployment workflow consists of:

```text
Selected Checkpoint
         │
         ▼
Load Deployment Model
         │
         ▼
Acquire Live Kinect Images
         │
         ▼
Semantic Segmentation
         │
         ▼
Center-Ratio Analysis
         │
         ▼
Robot Navigation Decision
```

During deployment, the segmentation model continuously processes live RGB or RGB-D camera frames captured by the Microsoft Kinect.

The generated semantic masks are analysed using the predefined center-ratio decision rule. Depending on the calculated ratio, the Pioneer P3-DX either:

- continues normal navigation; or
- performs a semantic glass-triggered stop.

This deployment stage provides practical validation of the benchmark models under real operating conditions and demonstrates how semantic segmentation can be integrated into a complete robotic perception pipeline.

Researchers who do not have access to the required deployment hardware may reproduce the benchmark experiments independently of this stage.

---

# 12. Expected Outputs

Each stage of the experimental workflow generates a collection of artefacts that document the progress and outcomes of the experiments.

Training and evaluation produce:

- configuration snapshots;
- training histories;
- validation results;
- held-out test metrics;
- selected model checkpoints;
- qualitative prediction outputs.

These artefacts are stored within the repository structure to support reproducibility and facilitate subsequent analysis.

The principal output locations are:

```text
outputs/
│
├── RGB/
│
└── RGBD/

results/
│
├── comparison_panels/
├── qualitative_analysis/
├── experiment_summary.csv
└── final_model_summary.txt
```

Together, these outputs provide a complete record of the benchmark experiments, including quantitative performance, qualitative visualisations, and the benchmark-selected checkpoints used during practical deployment.

Users reproducing the experiments are encouraged to review both the numerical metrics and the qualitative outputs to gain a comprehensive understanding of model performance rather than relying on a single evaluation criterion. :contentReference[oaicite:3]{index=3}

---

# 13. Reproducing the Published Results

The experiments described in this repository have been organised to allow researchers to reproduce the benchmark evaluation and practical deployment presented in the accompanying research paper.

To obtain results that are directly comparable with those reported in the study, users should follow the complete experimental workflow without modifying the model architecture, training configuration, dataset organisation, or evaluation procedure.

The recommended sequence is:

1. Install the required software dependencies.
2. Prepare the RGB-D GSD dataset.
3. Verify the dataset configuration files.
4. Train the RGB benchmark model.
5. Train the early-fusion RGB-D benchmark model.
6. Evaluate both selected checkpoints on the held-out test dataset.
7. Generate qualitative comparison panels.
8. Review the benchmark metrics and qualitative outputs.
9. Deploy the selected checkpoints on the Pioneer P3-DX platform (optional).

Following this workflow reproduces the benchmark-to-robot evaluation methodology adopted throughout this project.

---

# 14. Recommended Experiment Workflow

The complete experimental process is illustrated below.

```text
Repository Setup
        │
        ▼
Dataset Preparation
        │
        ▼
RGB Benchmark Training
        │
        ▼
RGB-D Benchmark Training
        │
        ▼
Validation and Checkpoint Selection
        │
        ▼
Held-Out Test Evaluation
        │
        ▼
Generate Qualitative Results
        │
        ▼
Review Benchmark Performance
        │
        ▼
Deploy on Pioneer P3-DX (Optional)
```

Each stage depends upon the successful completion of the previous stage. Running the experiments in this order ensures that benchmark evaluation, qualitative analysis, and deployment are performed using the same trained model checkpoints.

---

# 15. Common Issues

Most experimental failures occur during environment configuration rather than model training.

Common issues include:

### Dataset Path Errors

Incorrect dataset paths within the configuration files prevent the dataset loader from locating the RGB and depth images.

Verify that:

- dataset directories exist;
- manifest files are correctly referenced;
- configuration paths match the local dataset location.

---

### Missing Python Dependencies

If required libraries cannot be imported, reinstall the project dependencies using:

```bash
pip install -r requirements.txt
```

---

### CUDA Not Available

GPU acceleration is strongly recommended for model training.

Before beginning the benchmark experiments, verify CUDA availability:

```python
import torch
print(torch.cuda.is_available())
```

If CUDA is unavailable, training will execute on the CPU but may require substantially longer execution times.

---

### Practical Deployment

Deployment requires hardware that is not necessary for reproducing the benchmark experiments.

Researchers without access to:

- Pioneer P3-DX;
- Microsoft Kinect;
- compatible NVIDIA GPU;

may still reproduce all benchmark results, qualitative analyses, and quantitative comparisons presented in this repository.

---

# 16. Experiment Summary

This document has described the complete experimental workflow used to evaluate RGB and early-fusion RGB-D semantic segmentation for transparent glass detection.

Beginning with dataset preparation and benchmark training, the workflow progresses through validation, held-out benchmark evaluation, qualitative analysis, and practical deployment on a Pioneer P3-DX mobile robot.

The controlled experimental design ensures that both models are trained, evaluated, and deployed under identical conditions, allowing differences in performance to be attributed to the input modality rather than unrelated implementation factors.

Together with the accompanying methodology, deployment, and results documentation, this experiment guide provides a complete and reproducible description of the benchmark-to-robot evaluation framework developed in this project.