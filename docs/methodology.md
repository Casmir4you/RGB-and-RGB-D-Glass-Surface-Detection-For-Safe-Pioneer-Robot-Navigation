# Methodology and System Architecture

## Research Aim

The study investigates whether incorporating depth information into a transformer-based semantic segmentation model improves glass surface detection compared with RGB-only perception.

## Objectives

1. Develop an RGB SegFormer model for binary glass segmentation.
2. Extend SegFormer to accept four-channel RGB-D input.
3. Train both models using identical experimental settings.
4. Compare both models using Pixel Accuracy, Mean IoU, per-class IoU, Precision, Recall, and F1-score.
5. Perform qualitative analysis of predicted masks and overlays.
6. Deploy both models in a Pioneer P3-DX perception pipeline using Microsoft Kinect data.

## Dataset

The RGB-D Glass Surface Detection dataset was used for training, validation, and testing.

The project uses:

- RGB images
- depth images
- binary segmentation masks
- predefined training, validation, and test splits

The dataset is not stored in the repository because of its size.

## RGB Pipeline

```text
RGB image
   │
   ▼
SegFormer encoder
   │
   ▼
Segmentation decoder
   │
   ▼
Binary glass mask
```

The RGB model acts as the baseline.

## RGB-D Pipeline

```text
RGB image + depth image
          │
          ▼
Four-channel input
          │
          ▼
Modified SegFormer encoder
          │
          ▼
Segmentation decoder
          │
          ▼
Binary glass mask
```

The first input embedding layer was adapted from three to four channels. The pretrained RGB weights were retained, while the depth-channel weights were initialised from the mean of the pretrained RGB-channel weights.

## Training Strategy

Both models were trained using the same optimisation settings to support a fair comparison between modalities.

The training framework includes:

- transfer learning
- mixed-precision training
- learning-rate warm-up
- gradient clipping
- weight decay
- early stopping
- checkpoint selection using validation Mean IoU

The experiment configurations are stored in:

```text
configs/rgb.yaml
configs/rgbd.yaml
```

## Evaluation

The best validation checkpoint from each experiment was evaluated on the held-out test split.

Reported metrics include:

- Pixel Accuracy
- Mean Intersection over Union
- Glass IoU
- Background IoU
- Glass Precision
- Glass Recall
- Glass F1-score

## Qualitative Analysis

The repository contains:

- predicted masks
- overlay images
- RGB and RGB-D outputs
- comparison panels
- representative deployment outputs

A representative four-panel comparison is stored at:

```text
results/comparison_panels/00000210_comparison(1).png
```

## Deployment Architecture

The real-time deployment workflow is:

1. The Microsoft Kinect captures RGB and depth frames.
2. Sensor data are transferred to the Python deployment framework.
3. Input frames are preprocessed.
4. The RGB or RGB-D SegFormer model performs inference.
5. A binary glass mask is generated.
6. The detection result is supplied to the Pioneer P3-DX control interface.
7. The robot continues moving or stops according to the configured glass-detection rule.

The deployment demonstrates practical integration of the trained perception models. The repository does not claim to implement or evaluate a complete autonomous navigation stack.
