# Methodology

## 1. Introduction

This document describes the experimental methodology used to compare RGB-only and early-fusion RGB-D semantic segmentation for transparent glass detection. The study was designed to determine whether the inclusion of aligned depth information improves glass segmentation performance when all other experimental conditions are controlled.

Transparent glass presents a significant challenge for mobile robot perception because it often lacks stable visual texture and may simultaneously transmit, reflect, or distort surrounding objects. These properties can cause conventional perception systems to misinterpret glass doors, partitions, windows, and walls as traversable space. For a mobile robot operating in an indoor environment, such errors may lead to unsafe navigation decisions or collisions.

Although RGB-D perception is commonly assumed to provide more useful information than RGB-only perception, direct comparisons are often affected by multiple uncontrolled variables. Studies may use different model architectures, training schedules, preprocessing procedures, optimisation methods, or evaluation protocols for each modality. Under such conditions, it becomes difficult to determine whether any improvement is specifically caused by depth information.

To address this limitation, the present study adopts a controlled comparative methodology. Two closely matched SegFormer-B0 semantic segmentation models are evaluated:

- an RGB baseline model using three-channel colour input; and
- an early-fusion RGB-D model using a four-channel colour-and-depth input.

The two models share the same backbone, decoder, loss function, optimiser, learning-rate schedule, batch size, number of training epochs, validation strategy, checkpoint-selection criterion, dataset partitions, image resolution, and evaluation metrics. The only intentional architectural difference is the extension of the first input layer from three channels to four channels.

The study consists of two evaluation stages. The first stage measures segmentation performance on the RGB-D Glass Surface Detection dataset using quantitative and qualitative benchmark evaluation. The second stage deploys the trained models on a Pioneer P3-DX mobile robot to examine whether benchmark performance translates into useful real-world glass detection and navigation intervention behaviour.

The methodology therefore combines controlled computer-vision experimentation with practical robotic deployment. This enables the study to evaluate not only which model performs better on a held-out test set, but also how the models behave when integrated into a real mobile robot perception pipeline.

---

## 2. Research Objective and Experimental Questions

The primary objective of the study is to determine whether the inclusion of raw aligned depth information through early fusion improves transparent glass semantic segmentation when compared with an RGB-only baseline under otherwise identical experimental conditions.

The study addresses the following main research question:

> Does early-fusion RGB-D input improve transparent glass segmentation performance relative to RGB-only input when architecture, training, validation, and evaluation conditions are held constant?

The benchmark evaluation also considers the following supporting questions:

1. How do the RGB and RGB-D models compare in terms of Pixel Accuracy, Mean Intersection-over-Union, class-specific Intersection-over-Union, Precision, Recall, and F1-score?

2. Does the addition of depth improve detection of the glass class specifically, rather than only improving overall pixel classification?

3. Are differences observed during validation maintained when the selected models are evaluated on a held-out test set?

4. What types of segmentation errors are visible in representative qualitative predictions produced by each model?

5. Does benchmark performance correspond with reliable semantic glass detection during practical deployment on a Pioneer P3-DX mobile robot?

6. Does either model provide a more suitable balance between segmentation quality, inference latency, and semantic navigation-trigger consistency?

The study is not intended to prove that RGB or RGB-D perception is universally superior for every glass-detection system. Instead, it evaluates the specific effect of introducing raw depth as a fourth input channel within a controlled SegFormer-B0 early-fusion framework.

---

## 3. Overall Experimental Design

The experimental design follows a controlled comparative structure in which the RGB model serves as the baseline and the RGB-D model serves as the modified experimental condition.

The complete methodology consists of the following stages:

1. Preparation and verification of the RGBD-GSD dataset.
2. Creation of fixed training, validation, and test partitions.
3. Configuration of the RGB SegFormer-B0 baseline.
4. Adaptation of the SegFormer-B0 input layer for four-channel RGB-D input.
5. Training of both models under matched optimisation conditions.
6. Selection of the best checkpoint using validation Mean Intersection-over-Union.
7. Evaluation of the selected checkpoints on the held-out test set.
8. Generation of qualitative prediction masks, overlays, and comparison panels.
9. Deployment of both trained models on the Pioneer P3-DX robot.
10. Comparison of benchmark performance, inference behaviour, and semantic safety responses.

The benchmark stage and robot-deployment stage are treated as related but distinct forms of evaluation. Benchmark testing measures segmentation performance under controlled dataset conditions, while robot deployment examines how the trained models behave when exposed to live sensor input and integrated with a semantic navigation safety layer.

The high-level experimental workflow is shown below.

```text
RGBD-GSD Dataset
        │
        ▼
Training / Validation / Test Partitions
        │
        ├───────────────────────────────┐
        │                               │
        ▼                               ▼
RGB Input                         RGB + Depth Input
        │                               │
        ▼                               ▼
RGB SegFormer-B0             RGB-D SegFormer-B0
        │                               │
        ▼                               ▼
Matched Training and Validation Procedure
        │
        ▼
Best Checkpoint Selected by Validation mIoU
        │
        ▼
Held-Out Test Evaluation
        │
        ▼
Quantitative and Qualitative Comparison
        │
        ▼
Pioneer P3-DX Deployment
        │
        ▼
Semantic Detection and Navigation Intervention Analysis

---

## 4. Controlled Experimental Design

A fundamental objective of this study was to isolate the contribution of depth information to transparent glass semantic segmentation while minimising the influence of unrelated experimental variables. Rather than comparing different semantic segmentation architectures or independently optimised perception pipelines, the study adopts a controlled experimental design in which only a single variable is intentionally modified between the two experimental conditions.

The RGB model serves as the baseline configuration, while the RGB-D model represents the experimental condition. Both models are based on the SegFormer-B0 architecture and share identical training, validation, and evaluation procedures. The only architectural modification introduced into the RGB-D model is the extension of the first patch embedding layer to accept an additional depth channel.

Maintaining identical experimental conditions is essential because changes in optimisation strategy, network architecture, data augmentation, or evaluation methodology can independently influence segmentation performance. Without adequate control of these factors, it becomes difficult to determine whether observed improvements are genuinely attributable to depth information or instead arise from unrelated implementation differences.

The controlled methodology adopted in this study ensures that the comparison focuses exclusively on the effect of incorporating aligned depth information into the network input.

### 4.1 Baseline Configuration

The RGB baseline uses the standard SegFormer-B0 semantic segmentation architecture operating on conventional three-channel colour images.

The baseline configuration provides the reference point against which the early-fusion RGB-D model is evaluated. No architectural modifications are introduced beyond those already defined within the original SegFormer implementation.

The RGB model therefore represents a conventional semantic segmentation pipeline using only colour information for transparent glass detection.

### 4.2 Experimental Configuration

The experimental model extends the RGB baseline by introducing aligned depth information through an early-fusion strategy.

Instead of modifying the encoder, decoder, attention mechanism, or prediction head, the architecture is adapted only at the network input. The RGB image and corresponding depth image are concatenated to produce a four-channel input tensor consisting of:

```text
Red
Green
Blue
Depth
```

The modified tensor is processed by the same SegFormer-B0 backbone used by the RGB baseline.

No additional attention modules, fusion blocks, auxiliary supervision, or decoder modifications are introduced. Consequently, any differences observed between the two models can reasonably be attributed to the inclusion of the depth modality rather than changes elsewhere within the architecture.

---

## 5. Experimental Variables

The study follows the principles of controlled experimentation by identifying independent, dependent, and controlled variables before model development.

### 5.1 Independent Variable

The independent variable is the input modality supplied to the semantic segmentation network.

Two experimental conditions are evaluated:

| Experimental Condition | Input |
|-------------------------|-------|
| RGB | Three-channel colour image |
| RGB-D | Four-channel colour and aligned depth image |

This represents the only intentional difference between both experiments.

### 5.2 Dependent Variables

The dependent variables are the performance measures obtained after training and evaluation.

Benchmark evaluation includes:

- Pixel Accuracy
- Mean Intersection-over-Union (mIoU)
- Glass Intersection-over-Union
- Background Intersection-over-Union
- Precision
- Recall
- F1-score

Practical deployment additionally considers:

- inference latency,
- semantic detection consistency,
- navigation trigger behaviour,
- qualitative segmentation quality during robot operation.

These measurements provide complementary evidence regarding both benchmark performance and practical robotic usefulness.

### 5.3 Controlled Variables

To ensure a fair comparison, all remaining experimental conditions are held constant throughout the study.

The controlled variables include:

| Controlled Component | Identical for Both Models |
|----------------------|---------------------------|
| Backbone architecture | ✓ |
| Decoder architecture | ✓ |
| Dataset | ✓ |
| Training images | ✓ |
| Validation images | ✓ |
| Test images | ✓ |
| Image resolution | ✓ |
| Pre-processing | ✓ |
| Loss function | ✓ |
| Optimiser | ✓ |
| Learning rate | ✓ |
| Weight decay | ✓ |
| Batch size | ✓ |
| Mixed precision training | ✓ |
| Gradient clipping | ✓ |
| Early stopping | ✓ |
| Checkpoint selection criterion | ✓ |
| Evaluation metrics | ✓ |
| Hardware platform | ✓ |

Maintaining these controls reduces experimental bias and ensures that the resulting comparison reflects the influence of depth information rather than differences in model optimisation or implementation.

---

## 6. Experimental Fairness

Comparative evaluations of RGB and RGB-D perception frequently introduce multiple simultaneous modifications, including different backbone networks, fusion mechanisms, optimisation schedules, loss functions, or data augmentation strategies. While such approaches may improve absolute segmentation performance, they make it difficult to identify which component is responsible for the observed improvement.

The methodology adopted in this study intentionally avoids these confounding factors.

Both experimental conditions use the same implementation, the same source code, identical optimisation parameters, identical training schedules, and identical evaluation procedures. The RGB-D model differs only through the addition of a fourth input channel representing aligned depth information.

This design strengthens the internal validity of the comparison by ensuring that performance differences are directly attributable to the investigated variable rather than unrelated methodological differences.

Consequently, the results provide a more reliable assessment of the practical value of early-fusion RGB-D input for transparent glass semantic segmentation.

---

---

# 7. Dataset

The benchmark experiments were conducted using the **RGB-D Glass Surface Detection (RGBD-GSD)** dataset, a publicly available semantic segmentation dataset specifically developed for transparent glass detection. The dataset provides aligned RGB images, depth images, and pixel-level ground-truth annotations, making it suitable for evaluating both RGB-only and RGB-D semantic segmentation models under identical experimental conditions.

Unlike general semantic segmentation datasets that contain multiple object categories, the RGBD-GSD dataset focuses specifically on transparent glass surfaces. This makes it particularly appropriate for investigating perception challenges associated with glass doors, partitions, windows, and other transparent obstacles commonly encountered in indoor robotic environments.

Each sample within the dataset contains three complementary data modalities:

- an RGB colour image;
- an aligned depth image; and
- a binary semantic segmentation mask identifying transparent glass regions.

The use of aligned RGB and depth images enables direct comparison between RGB-only and RGB-D perception while ensuring that both models observe exactly the same physical scene during training and evaluation.

The segmentation task is formulated as a binary semantic segmentation problem consisting of two classes:

| Class | Label |
|---------|------:|
| Background | 0 |
| Glass | 1 |

Pixels outside the labelled regions are assigned the dataset ignore index where appropriate and are excluded from metric computation during training and evaluation.

---

# 8. Dataset Organisation

To ensure reproducibility, the dataset was organised using fixed training, validation, and testing partitions.

The complete dataset contains **3,009 annotated samples**, divided into three mutually exclusive subsets:

| Dataset Split | Number of Samples |
|---------------|-----------------:|
| Training | 2,040 |
| Validation | 360 |
| Testing | 609 |

The training partition is used exclusively for parameter optimisation, the validation partition is used for checkpoint selection and early stopping, and the testing partition is reserved for the final benchmark evaluation.

No images are shared between dataset partitions, preventing information leakage during model development and ensuring that benchmark results accurately represent model generalisation to previously unseen scenes.

The same dataset partitions are used for both RGB and RGB-D experiments. Consequently, every RGB image evaluated by the baseline model corresponds exactly to the RGB image evaluated by the RGB-D model, with the latter additionally receiving the aligned depth image.

Maintaining identical dataset partitions across both experimental conditions ensures that any observed performance differences arise from the investigated input modality rather than variations in training or testing data.

---

# 9. Dataset Directory Structure

The dataset is organised into separate directories containing RGB images, aligned depth images, and semantic segmentation masks.

A simplified representation of the expected dataset organisation is shown below.

```text
RGBD-GSD/
│
├── train/
│   ├── rgb/
│   ├── depth/
│   └── masks/
│
├── validation/
│   ├── rgb/
│   ├── depth/
│   └── masks/
│
└── test/
    ├── rgb/
    ├── depth/
    └── masks/
```

Each RGB image is paired with a corresponding depth image and segmentation mask using identical filenames, allowing the dataset loader to retrieve all modalities for each sample without ambiguity.

This organisation simplifies data loading while ensuring consistent alignment between colour, depth, and annotation data.

---

# 10. Data Loading Pipeline

A unified dataset loader is implemented to support both experimental conditions while maintaining a common training pipeline.

Instead of maintaining separate implementations for RGB and RGB-D experiments, a single dataset loader dynamically prepares the required input depending on the selected configuration file.

The data loading process follows the sequence illustrated below.

```text
Dataset
      │
      ▼
Read RGB Image
      │
      ▼
Read Segmentation Mask
      │
      ▼
Read Depth Image (RGB-D only)
      │
      ▼
Apply Pre-processing
      │
      ▼
Generate Input Tensor
      │
      ▼
Return Training Sample
```

When the RGB configuration is selected, only the RGB image and corresponding segmentation mask are loaded.

When the RGB-D configuration is selected, the aligned depth image is additionally loaded and concatenated with the RGB image to produce a four-channel input tensor.

Using a unified dataset loader ensures that preprocessing, augmentation, annotation handling, and batching remain identical across both experimental conditions.

---

# 11. Data Pre-processing

Before training, each input sample undergoes a series of preprocessing operations designed to produce consistent input tensors while preserving the alignment between RGB images, depth images, and segmentation masks.

The preprocessing pipeline includes:

- image loading;
- depth image loading (RGB-D only);
- segmentation mask loading;
- image resizing;
- tensor conversion;
- normalisation;
- batching.

For RGB experiments, only the three colour channels are processed.

For RGB-D experiments, the aligned depth image is processed together with the RGB image before concatenation into a four-channel tensor.

Throughout preprocessing, care is taken to preserve pixel-wise alignment between RGB images, depth maps, and semantic masks. Maintaining accurate alignment is essential because even small spatial inconsistencies between modalities could introduce incorrect supervision during training and negatively affect segmentation performance.

The preprocessing pipeline therefore applies identical geometric transformations to all modalities simultaneously whenever spatial operations are required.

---

# 12. Data Integrity Verification

Prior to training, the dataset is inspected to verify that all required files are present and correctly aligned.

Automated inspection utilities are used to identify potential issues such as:

- missing RGB images;
- missing depth images;
- missing segmentation masks;
- mismatched filenames;
- inconsistent image dimensions;
- corrupted image files;
- incorrect depth alignment.

Representative RGB images, depth maps, and segmentation masks are also visually inspected to confirm that the annotated glass regions correspond correctly with the underlying scene.

Additional verification is performed on the depth channel to ensure that valid depth measurements are available throughout the dataset and that the depth images are correctly associated with their corresponding RGB images.

Performing these integrity checks before training reduces the likelihood of introducing avoidable dataset errors that could adversely affect optimisation or bias benchmark evaluation.

The repository provides dedicated inspection scripts to assist with these verification procedures before any model training is initiated.

---

---

# 13. Model Architecture

The experimental framework is based on the SegFormer-B0 semantic segmentation architecture. SegFormer was selected because it combines transformer-based feature extraction with a lightweight decoder, enabling accurate semantic segmentation while maintaining computational efficiency suitable for practical robotic deployment.

Unlike conventional convolutional neural networks, SegFormer employs a hierarchical vision transformer encoder capable of learning multi-scale feature representations through self-attention. The architecture captures both local image details and long-range contextual information without relying on positional encoding, making it robust to variations in scene layout and object scale.

The decoder is intentionally lightweight, fusing multi-scale encoder features to produce dense pixel-level segmentation predictions. This design reduces computational complexity while maintaining competitive segmentation accuracy, making SegFormer-B0 particularly suitable for applications requiring real-time inference.

The present study uses SegFormer-B0 as the common backbone for both RGB and RGB-D experiments. Keeping the backbone identical ensures that any observed performance differences are attributable to the investigated input modality rather than differences in network architecture.

The overall architecture is illustrated below.

```text
Input Image
      │
      ▼
Patch Embedding
      │
      ▼
Hierarchical Transformer Encoder
      │
      ▼
Multi-scale Feature Extraction
      │
      ▼
Lightweight Decoder
      │
      ▼
Pixel-wise Glass Segmentation
```

Both experimental models follow this architecture without modification beyond the network input layer.

---

# 14. RGB Baseline Model

The RGB baseline represents the reference model used throughout the comparative evaluation.

The model receives a conventional three-channel RGB image as input and performs binary semantic segmentation to classify each pixel as either **glass** or **background**.

The baseline architecture consists of:

- standard SegFormer-B0 encoder;
- lightweight SegFormer decoder;
- binary segmentation head;
- ImageNet-pretrained backbone weights.

No architectural modifications are introduced into the RGB model.

The RGB baseline therefore represents a conventional transformer-based semantic segmentation model operating solely on colour information.

Its primary purpose within the study is to provide a controlled reference against which the early-fusion RGB-D model can be evaluated.

---

# 15. Early-Fusion RGB-D Model

The experimental model extends the RGB baseline by incorporating aligned depth information through an early-fusion strategy.

Rather than processing colour and depth independently, the RGB image and corresponding depth image are combined before entering the network.

The resulting input tensor consists of four channels:

```text
Red
Green
Blue
Depth
```

The complete four-channel tensor is processed directly by the SegFormer encoder, allowing the transformer to learn joint colour-depth feature representations from the earliest stage of feature extraction.

This approach differs from late-fusion architectures in which colour and depth are processed independently before feature fusion.

The early-fusion strategy was selected for three principal reasons.

First, it introduces only a minimal architectural modification, preserving the controlled nature of the comparison.

Second, it enables direct comparison with the RGB baseline while avoiding additional fusion modules that could independently influence performance.

Third, it maintains computational simplicity, making the approach suitable for practical deployment on resource-constrained robotic platforms.

Apart from the modified input layer, the RGB-D model is architecturally identical to the RGB baseline.

---

# 16. Modification of the Input Layer

Supporting RGB-D input requires only a single architectural modification.

The first patch embedding layer of SegFormer-B0 is extended from three input channels to four input channels.

This modification allows the network to accept an additional aligned depth channel while preserving the remainder of the architecture unchanged.

The transformation can be summarised as:

```text
RGB Baseline

Input
3 Channels
(R,G,B)

↓

Patch Embedding

↓

Transformer Encoder


RGB-D Model

Input
4 Channels
(R,G,B,D)

↓

Modified Patch Embedding

↓

Same Transformer Encoder
```

No additional encoder layers, decoder components, attention mechanisms, skip connections, or prediction heads are introduced.

Consequently, the comparison isolates the influence of depth information without introducing unnecessary architectural complexity.

---

# 17. Weight Initialisation Strategy

Both experimental models utilise transfer learning to accelerate convergence and improve optimisation stability.

The RGB baseline directly uses ImageNet-pretrained SegFormer-B0 weights.

For the RGB-D model, the pretrained weights corresponding to the original RGB channels are retained without modification.

Because pretrained ImageNet models contain no parameters for an additional depth channel, a new set of weights must be initialised for the fourth input channel.

Rather than applying random initialisation, the depth-channel weights are initialised using the mean of the pretrained RGB filter weights.

This strategy preserves the statistical characteristics of the pretrained feature extractor while enabling the network to incorporate depth information from the beginning of training.

The initialisation procedure may be summarised as:

```text
Pretrained RGB Filters

R
G
B

↓

Mean Filter

↓

Initial Depth Filter

↓

4-Channel Patch Embedding
```

Retaining pretrained RGB weights while carefully initialising the depth channel improves optimisation stability and avoids discarding knowledge learned from large-scale natural image datasets.

---

# 18. Rationale for Early Fusion

Several strategies exist for combining RGB and depth information within semantic segmentation networks, including early fusion, middle fusion, and late fusion.

Early fusion was selected for this study because it provides the simplest possible extension of the RGB baseline while preserving a controlled experimental design.

More sophisticated fusion mechanisms often introduce additional convolutional layers, attention modules, cross-modal interaction blocks, or multi-branch encoder architectures. Although such approaches may improve segmentation performance, they simultaneously introduce multiple additional variables that complicate fair comparison.

The objective of the present study is not to identify the highest-performing RGB-D architecture, but rather to determine whether the addition of raw aligned depth information alone provides measurable benefit.

By selecting an early-fusion strategy, the study ensures that:

- both models remain nearly identical;
- architectural complexity is minimised;
- implementation differences are reduced;
- computational cost remains comparable;
- observed performance differences can be attributed primarily to the input modality.

This design strengthens the internal validity of the comparison and provides a clearer assessment of the contribution of depth information to transparent glass semantic segmentation.

---

---

# 19. Training Configuration

To ensure a fair comparison between the RGB and RGB-D models, both networks were trained using identical optimisation settings. Maintaining consistent training conditions ensures that any observed differences in segmentation performance are attributable to the input modality rather than variations in the training procedure.

Both models were trained using the same hardware platform, software environment, optimisation strategy, learning rate schedule, stopping criteria, and evaluation protocol. The only intentional difference between the experiments was the number of input channels supplied to the network.

Table 1 summarises the principal training configuration used throughout the study.

| Parameter | Value |
|-----------|------|
| Backbone | SegFormer-B0 |
| Task | Binary Semantic Segmentation |
| Classes | Background, Glass |
| Epochs | 50 |
| Batch Size | 2 |
| Learning Rate | 6 × 10⁻⁵ |
| Weight Decay | 0.02 |
| Optimiser | AdamW |
| Warm-up Epochs | 3 |
| Mixed Precision | Enabled |
| Gradient Clipping | 1.0 |
| Early Stopping Patience | 12 Epochs |
| Checkpoint Selection | Highest Validation mIoU |

The selected configuration represents a balance between optimisation stability, computational efficiency, and generalisation performance while remaining compatible with the available GPU resources.

---

# 20. Hyperparameter Selection

Hyperparameters were selected before the commencement of the comparative experiments and remained fixed throughout all training runs.

Rather than independently tuning each model, identical hyperparameters were intentionally maintained for both the RGB and RGB-D experiments. This approach prevents model-specific optimisation from introducing experimental bias and ensures that the comparison evaluates the effect of the input modality rather than differences in hyperparameter tuning.

The learning rate was selected to provide stable convergence when fine-tuning ImageNet-pretrained transformer weights. A relatively small learning rate reduces the risk of destroying previously learned feature representations while allowing gradual adaptation to the glass segmentation task.

The batch size of four images was determined by available GPU memory while maintaining stable optimisation. Mixed precision training enabled efficient memory utilisation, allowing larger effective workloads without compromising numerical stability.

Weight decay was included to reduce overfitting by discouraging excessively large parameter values during optimisation. Early stopping further improved generalisation by preventing unnecessary training once validation performance ceased improving.

Maintaining these hyperparameters across both experimental conditions ensures methodological consistency and strengthens the validity of the comparative evaluation.

---

# 21. Loss Function

Both models were trained using the same semantic segmentation loss function.

The objective of the loss function is to minimise disagreement between the predicted segmentation map and the corresponding ground-truth annotation during optimisation.

For each training sample, the predicted probability distribution produced by the segmentation head is compared with the pixel-level class labels contained within the ground-truth segmentation mask.

Only valid labelled pixels contribute to the optimisation process. Pixels assigned the dataset ignore index are excluded from loss computation, ensuring that ambiguous or intentionally unlabeled regions do not influence gradient updates.

Using an identical loss function for both experimental conditions ensures that optimisation remains consistent throughout the comparative study.

---

# 22. Optimisation Strategy

Parameter optimisation is performed using the AdamW optimiser.

AdamW combines adaptive learning-rate estimation with decoupled weight decay, making it well suited to transformer-based architectures such as SegFormer. Compared with conventional stochastic gradient descent, AdamW typically provides more stable convergence during fine-tuning of pretrained vision transformers.

The optimiser updates all trainable parameters simultaneously during each optimisation step using gradients computed through backpropagation.

Throughout the study, the optimiser configuration remains unchanged for both the RGB and RGB-D experiments. Maintaining identical optimisation behaviour ensures that any observed performance differences are attributable to the investigated input modality rather than differences in parameter update strategies.

---

# 23. Learning Rate Schedule

A fixed initial learning rate of **6 × 10⁻⁵** is used for all experiments.

To improve optimisation stability during the initial phase of training, a three-epoch linear warm-up schedule is employed. During this period, the learning rate increases gradually from a small initial value until the target learning rate is reached.

The warm-up process reduces the risk of unstable parameter updates during the early stages of optimisation, particularly when fine-tuning pretrained transformer models.

Following the warm-up period, optimisation proceeds using the established learning rate for the remainder of training unless terminated by the early stopping criterion.

The same learning-rate schedule is applied to both experimental conditions, ensuring consistency throughout the comparative evaluation.

The learning-rate schedule is illustrated conceptually below.

```text
Learning Rate

│
│                ───────────────────────────────
│               │
│              │
│             │
│            │
│           │
│__________│_____________________________________

      Warm-up              Remaining Training
      (3 Epochs)
```

---

# 24. Mixed Precision Training

Mixed precision training is employed to improve computational efficiency while maintaining numerical accuracy.

Instead of performing all computations using single-precision floating-point arithmetic, mixed precision selectively uses lower-precision operations where appropriate while preserving higher precision for numerically sensitive calculations.

This approach provides several practical advantages:

- reduced GPU memory consumption;
- faster training;
- increased computational throughput;
- improved hardware utilisation.

Automatic loss scaling is used throughout training to minimise the risk of numerical underflow during gradient computation.

Both RGB and RGB-D models utilise identical mixed precision settings, ensuring that computational efficiency remains comparable across experiments.

---

# 25. Gradient Clipping

Gradient clipping is applied during optimisation using a maximum gradient norm of **1.0**.

Transformer architectures occasionally produce unusually large gradients during optimisation. If left unchecked, these gradients may destabilise training and slow convergence.

Gradient clipping limits the magnitude of parameter updates while preserving the overall optimisation direction.

Applying the same clipping threshold throughout both experiments contributes to stable convergence without introducing differences between the RGB and RGB-D training procedures.

---

# 26. Early Stopping

To reduce overfitting, early stopping is incorporated into the training procedure.

Validation performance is monitored after each training epoch using Mean Intersection-over-Union (mIoU). If validation performance fails to improve for twelve consecutive epochs, training is terminated automatically.

This strategy prevents unnecessary optimisation after the model has converged while reducing the likelihood of overfitting the training data.

The early stopping procedure follows the workflow below.

```text
Train Epoch

↓

Evaluate Validation Set

↓

Validation mIoU Improved?

        │
   ┌────┴────┐
   │         │
 Yes        No
   │         │
 Save     Increase
 Model    Patience Counter
   │         │
   └────┬────┘
        │
 Patience Reached?
        │
   ┌────┴────┐
   │         │
  No       Yes
   │         │
Continue   Stop Training
```

---

# 27. Checkpoint Selection

Rather than selecting the final training epoch, the best-performing model is determined using validation Mean Intersection-over-Union.

After each epoch, the current model is evaluated on the validation dataset. If the validation mIoU exceeds the best value previously observed, the model parameters are saved as the current best checkpoint.

Only this best-performing checkpoint is subsequently evaluated on the held-out test dataset.

Selecting checkpoints according to validation performance rather than training completion reduces the influence of overfitting and ensures that the reported benchmark results correspond to the model demonstrating the strongest generalisation during training.

Using an identical checkpoint selection criterion for both experimental conditions further strengthens the fairness and reproducibility of the comparative evaluation.

---

---

# 28. Evaluation Methodology

Following completion of training, the selected checkpoints are evaluated using both benchmark testing and practical robotic deployment. These complementary evaluation stages provide quantitative evidence of segmentation performance together with qualitative observations of model behaviour in realistic operating conditions.

The benchmark evaluation measures segmentation accuracy using the held-out test partition of the RGBD-GSD dataset. Since these images are not used during training or validation, they provide an unbiased assessment of each model's ability to generalise to previously unseen scenes.

Practical deployment evaluates how the trained models perform when integrated into the perception pipeline of a Pioneer P3-DX mobile robot. Unlike benchmark testing, deployment focuses on real-time semantic perception, inference behaviour, and navigation support rather than solely numerical performance metrics.

The evaluation framework therefore consists of two complementary stages:

1. Controlled benchmark evaluation using the RGBD-GSD test dataset.
2. Practical deployment using live sensor data collected by the Pioneer P3-DX platform.

---

# 29. Quantitative Evaluation Metrics

Model performance is assessed using several complementary evaluation metrics commonly employed in semantic segmentation. No single metric fully characterises segmentation quality; therefore, multiple measures are reported to provide a comprehensive assessment of performance.

The primary evaluation metric is **Mean Intersection-over-Union (mIoU)**, which measures the average overlap between predicted segmentation masks and ground-truth annotations across all classes.

Additional metrics include:

- Pixel Accuracy
- Glass Intersection-over-Union
- Background Intersection-over-Union
- Precision
- Recall
- F1-score

These metrics capture different aspects of segmentation performance and allow a more detailed comparison between the RGB and RGB-D models.

### 29.1 Pixel Accuracy

Pixel Accuracy measures the proportion of correctly classified pixels across the entire image.

Although Pixel Accuracy provides an overall indication of prediction quality, it may overestimate performance in datasets where one class occupies substantially more pixels than another. In the RGBD-GSD dataset, background pixels are generally more numerous than glass pixels; therefore, Pixel Accuracy is interpreted alongside class-specific metrics.

### 29.2 Mean Intersection-over-Union

Mean Intersection-over-Union is the principal evaluation metric used throughout this study.

For each class, the predicted segmentation mask is compared with the ground-truth annotation by measuring the overlap relative to the union of both regions.

The mean value across all classes provides a balanced measure of segmentation performance that accounts for both false positives and false negatives.

Validation mIoU is also used as the criterion for checkpoint selection during training.

### 29.3 Class-specific Intersection-over-Union

In addition to overall mIoU, Intersection-over-Union is reported separately for the two semantic classes.

These include:

- Glass IoU
- Background IoU

Glass IoU is particularly important because the primary objective of the study is accurate transparent glass detection. Reporting class-specific IoU allows improvements or degradations in glass segmentation to be identified even when overall performance appears similar.

### 29.4 Precision

Precision measures the proportion of pixels predicted as glass that are actually glass.

High precision indicates that relatively few background pixels are incorrectly classified as transparent glass.

For robotic navigation, high precision reduces unnecessary avoidance behaviour caused by false detections.

### 29.5 Recall

Recall measures the proportion of true glass pixels successfully detected by the model.

High recall indicates that fewer transparent obstacles are missed during segmentation.

From a navigation safety perspective, recall is particularly important because undetected glass surfaces may increase collision risk.

### 29.6 F1-score

The F1-score combines Precision and Recall into a single performance measure by balancing both false positives and false negatives.

Because transparent glass occupies relatively small image regions in many scenes, the F1-score provides an informative measure of segmentation quality for the target class.

---

# 30. Qualitative Evaluation

Numerical metrics provide valuable information regarding segmentation accuracy but do not fully describe model behaviour. Consequently, qualitative evaluation is performed alongside quantitative benchmark testing.

Representative test images are selected to compare:

- RGB input images;
- ground-truth segmentation masks;
- RGB model predictions;
- RGB-D model predictions;
- overlay visualisations;
- side-by-side comparison panels.

Visual inspection focuses on several aspects of segmentation quality, including:

- boundary accuracy;
- continuity of detected glass surfaces;
- missed glass regions;
- false positive detections;
- prediction consistency across different scene types.

These qualitative comparisons provide insight into the types of errors produced by each model and help explain differences observed in the quantitative evaluation metrics.

Representative qualitative examples are included within the repository under the `results/qualitative_analysis` directory.

---

# 31. Practical Robot Deployment

Following benchmark evaluation, both trained models are deployed on a Pioneer P3-DX mobile robot to investigate their behaviour during practical operation.

The deployment system integrates the trained segmentation model into a real-time perception pipeline capable of processing live camera images and producing semantic glass segmentation masks during robot operation.

The deployment pipeline follows the sequence shown below.

```text
Camera
   │
   ▼
Image Acquisition
   │
   ▼
Pre-processing
   │
   ▼
SegFormer Inference
   │
   ▼
Glass Segmentation Mask
   │
   ▼
Semantic Safety Layer
   │
   ▼
Navigation Decision
```

Rather than replacing the robot's existing navigation system, the segmentation model functions as an additional semantic perception layer capable of identifying transparent obstacles that may not be reliably detected using conventional navigation sensors alone.

The deployment stage demonstrates the practical feasibility of integrating transformer-based semantic segmentation into a mobile robotic perception framework.

---

# 32. Inference Performance

In addition to segmentation quality, the computational performance of both models is considered during deployment.

The following characteristics are observed:

- inference latency;
- prediction stability;
- responsiveness during continuous operation;
- consistency of generated segmentation masks.

These factors influence the suitability of each model for real-time robotic perception.

Lower inference latency enables more frequent environmental updates, while stable prediction behaviour contributes to reliable navigation decisions.

Although benchmark accuracy remains the primary focus of the study, computational efficiency is recognised as an important consideration for practical deployment on autonomous mobile robots.

---

# 33. Reproducibility

Reproducibility is a central objective of the experimental methodology.

To facilitate independent verification of the reported results, the repository provides:

- complete source code;
- configuration files;
- training scripts;
- evaluation scripts;
- deployment scripts;
- documentation;
- representative qualitative outputs.

Both experimental conditions are executed using the same software environment, hardware platform, dataset partitions, and optimisation procedures. Configuration files define all major training parameters, allowing the experiments to be reproduced with minimal modification.

The repository structure has been organised to separate source code, configuration files, trained outputs, deployment utilities, and experimental results, simplifying replication of the complete experimental workflow.

---

# 34. Experimental Limitations

Although every effort has been made to ensure methodological fairness, several limitations should be acknowledged.

First, the comparison is restricted to the SegFormer-B0 architecture. Consequently, the findings should not be interpreted as general conclusions regarding all semantic segmentation networks.

Second, the study evaluates a single early-fusion strategy. Alternative fusion approaches, such as middle fusion, late fusion, or cross-modal attention mechanisms, may produce different performance characteristics.

Third, practical deployment is performed using a Pioneer P3-DX mobile robot within controlled indoor environments. Additional evaluation across a broader range of robots, sensors, and operating conditions would further strengthen external validity.

Finally, the study focuses on binary transparent glass segmentation. Future work may extend the methodology to include multiple transparent object categories, additional sensor modalities, or more complex semantic scene understanding tasks.

These limitations provide opportunities for future research while not affecting the validity of the controlled comparative evaluation presented in this work.

---

# 35. Methodology Summary

This methodology establishes a controlled experimental framework for comparing RGB-only and early-fusion RGB-D semantic segmentation for transparent glass detection.

By maintaining identical datasets, architectures, optimisation procedures, training schedules, validation strategies, and evaluation protocols, the study isolates the contribution of aligned depth information as the sole independent variable. The methodology combines rigorous benchmark testing with practical deployment on a Pioneer P3-DX mobile robot, enabling assessment of both segmentation accuracy and real-world applicability.

The resulting framework provides a transparent, reproducible, and scientifically controlled basis for evaluating the effectiveness of RGB and RGB-D perception in safe mobile robot navigation around transparent glass surfaces.