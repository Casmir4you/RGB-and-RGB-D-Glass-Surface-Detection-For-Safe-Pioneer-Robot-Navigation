# Results and Interpretation

## 1. Introduction

This document presents the experimental results obtained from the controlled comparison of RGB and early-fusion RGB-D semantic segmentation models for transparent glass detection. The results include quantitative benchmark evaluation, qualitative visual assessment, and practical robot deployment outcomes.

The purpose of the evaluation is not only to determine which model achieved the highest segmentation accuracy, but also to investigate how benchmark performance translates into real-world robotic behaviour. Although semantic segmentation metrics provide an objective measure of model performance, practical deployment introduces additional considerations such as inference efficiency, threshold robustness, and the consistency of navigation decisions.

The evaluation therefore follows the benchmark-to-robot methodology described in the accompanying research paper, combining offline benchmark experiments with real-time deployment on a Pioneer P3-DX mobile robot. Together, these complementary evaluations provide a more comprehensive assessment of transparent glass perception than benchmark testing alone. :contentReference[oaicite:1]{index=1}

---

# 2. Benchmark Evaluation Overview

Benchmark evaluation was performed using the held-out test partition of the RGB-D Glass Surface Detection (RGB-D GSD) dataset. Both the RGB and early-fusion RGB-D SegFormer-B0 models were trained using identical optimisation settings and evaluated under the same experimental conditions.

The benchmark experiments measured each model using standard semantic segmentation metrics:

- Pixel Accuracy
- Mean Intersection over Union (mIoU)
- Glass Intersection over Union (Glass IoU)
- Background Intersection over Union
- Glass Precision
- Glass Recall
- Glass F1-score

Using identical evaluation metrics ensures that both models are compared fairly and that any observed differences arise from the input modality rather than variations in the evaluation procedure.

The benchmark results provide the quantitative foundation for the subsequent qualitative analysis and practical robot deployment experiments.

---

# 3. Quantitative Benchmark Results

## Overall Performance

The held-out benchmark results for both models are summarised below.

| Metric | RGB | RGB-D | Better Model |
|---------|----:|------:|:------------|
| Pixel Accuracy | **0.9429** | 0.9408 | RGB |
| Mean IoU | **0.8152** | 0.8085 | RGB |
| Glass IoU | **0.6961** | 0.6850 | RGB |
| Background IoU | **0.9344** | 0.9321 | RGB |
| Glass Precision | **0.8358** | 0.8333 | RGB |
| Glass Recall | **0.8063** | 0.7938 | RGB |
| Glass F1-score | **0.8208** | 0.8131 | RGB |

Across all reported benchmark metrics, the RGB model achieved slightly higher performance than the early-fusion RGB-D model. Although the numerical differences are relatively small, they were consistent across every reported metric, indicating that the RGB model provided the strongest overall segmentation performance under the evaluated experimental conditions. :contentReference[oaicite:2]{index=2}

---

## Metric Interpretation

Each reported metric captures a different aspect of segmentation performance.

### Pixel Accuracy

Pixel Accuracy measures the proportion of correctly classified pixels across the entire image. Both models achieved values above 94%, demonstrating that the majority of image pixels were assigned the correct semantic label.

### Mean Intersection over Union (mIoU)

Mean IoU is generally regarded as the principal evaluation metric for semantic segmentation because it measures the overlap between predicted regions and ground-truth annotations while penalising both false positives and false negatives.

The RGB model achieved a mean IoU of **0.8152**, compared with **0.8085** for the RGB-D model, indicating slightly better overall segmentation quality.

### Glass IoU

Glass IoU is particularly important because transparent glass represents the target class for this study.

The RGB model achieved a Glass IoU of **0.6961**, outperforming the RGB-D model (**0.6850**). Although the difference is modest, improved Glass IoU indicates more accurate localisation of transparent glass surfaces.

### Precision and Recall

Precision measures the proportion of predicted glass pixels that were actually glass, whereas recall measures the proportion of true glass pixels successfully identified by the model.

The RGB model achieved slightly higher values for both precision and recall, indicating a more favourable balance between missed detections and false-positive predictions.

### F1-score

The F1-score combines precision and recall into a single performance measure.

The RGB model achieved the highest Glass F1-score (**0.8208**), suggesting the most balanced segmentation performance for the target class.

---

# 4. Overall Interpretation

Several important observations emerge from the benchmark evaluation.

First, both models achieved strong semantic segmentation performance, demonstrating that transformer-based architectures are capable of accurately identifying transparent glass surfaces using either RGB or early-fusion RGB-D input.

Second, the successful training and evaluation of the four-channel RGB-D SegFormer confirms that early multimodal fusion can be implemented within the SegFormer architecture without requiring changes to the encoder beyond the modified input projection layer.

Finally, contrary to the initial hypothesis, incorporating depth information did not improve benchmark performance under the evaluated conditions. Instead, the RGB model consistently achieved slightly higher values across every reported evaluation metric.

As discussed in the accompanying paper, several plausible factors may have contributed to this outcome, including unreliable depth measurements on transparent surfaces, sensor noise, increased multimodal learning complexity, and limitations associated with the available benchmark dataset. These explanations are informed interpretations of the observed results rather than experimentally isolated causal mechanisms. :contentReference[oaicite:3]{index=3}

---

# 5. Comparative Analysis

## RGB versus Early-Fusion RGB-D

The benchmark evaluation demonstrates that both the RGB and early-fusion RGB-D models achieved strong semantic segmentation performance for transparent glass detection. However, the RGB model consistently outperformed the RGB-D model across every reported evaluation metric.

Although the numerical differences between the two models were relatively small, they were remarkably consistent. The RGB model achieved higher Pixel Accuracy, Mean Intersection over Union (mIoU), Glass IoU, Precision, Recall, and F1-score on the held-out test dataset.

This consistency suggests that, under the evaluated experimental conditions, adding depth information through early fusion did not improve segmentation performance. Instead, the RGB model provided the strongest overall balance between segmentation accuracy and computational simplicity. :contentReference[oaicite:1]{index=1}

Rather than viewing this result as a limitation of RGB-D perception, it should be interpreted within the context of the specific dataset, sensor characteristics, fusion strategy, and network architecture used in this study.

---

## Per-Metric Comparison

Examining each evaluation metric individually provides additional insight into model behaviour.

### Pixel Accuracy

The RGB model achieved a slightly higher Pixel Accuracy (0.9429) than the RGB-D model (0.9408). While the difference is small, it indicates that the RGB model correctly classified a marginally greater proportion of pixels across the test dataset.

### Mean Intersection over Union

Mean IoU is the primary benchmark metric because it measures the overlap between predicted segmentation masks and the corresponding ground-truth annotations.

The RGB model achieved the highest Mean IoU (0.8152), indicating superior overall segmentation quality across both semantic classes.

### Glass IoU

Glass IoU is particularly important because transparent glass represents the target object of interest.

The RGB model achieved a Glass IoU of 0.6961 compared with 0.6850 for the RGB-D model. This result suggests that the RGB model produced slightly more accurate localisation of transparent glass surfaces.

### Precision

Both models demonstrated high precision, indicating that when glass was predicted, the prediction was usually correct.

The RGB model achieved a marginally higher precision, indicating slightly fewer false-positive glass predictions.

### Recall

Recall measures how successfully the model identified the complete extent of glass regions.

The RGB model achieved the highest recall, suggesting that it detected a greater proportion of true glass pixels than the RGB-D model.

### F1-score

The Glass F1-score combines precision and recall into a single balanced metric.

The RGB model achieved the highest F1-score, indicating the strongest overall performance for the target class.

Taken together, these metrics consistently favour the RGB model while confirming that both models achieved competitive semantic segmentation performance. :contentReference[oaicite:2]{index=2}

---

## Interpreting the Performance Difference

The original hypothesis of this study proposed that incorporating depth information would improve transparent glass segmentation by providing additional geometric cues.

However, the benchmark results did not support this hypothesis under the evaluated conditions.

Several factors may plausibly explain the observed outcome.

Transparent glass presents a well-known challenge for active depth sensors because transmitted and reflected infrared light often produces incomplete or noisy depth measurements. Consequently, the additional depth channel may contribute less useful information than expected when compared with high-quality RGB appearance features.

Furthermore, early fusion combines RGB and depth information before feature extraction. While this approach enables the network to learn joint multimodal representations, it also requires the model to learn from two modalities that may differ substantially in reliability, particularly around transparent surfaces.

The RGB model, in contrast, relies exclusively on visual appearance cues such as edges, reflections, and scene context. These features appear to have provided sufficient information for accurate segmentation within the evaluated benchmark dataset.

It is important to emphasise that these explanations represent informed interpretations of the observed results rather than experimentally isolated causal mechanisms. Additional experiments using different datasets, sensors, or fusion strategies would be required to determine the precise contribution of each factor. :contentReference[oaicite:3]{index=3}

---

# 6. Qualitative Evaluation

While benchmark metrics provide an objective measure of segmentation quality, qualitative evaluation allows the predicted segmentation masks to be examined visually.

Visual inspection is particularly valuable for transparent object detection because it reveals how accurately the predicted glass regions correspond to the annotated ground truth and highlights strengths or weaknesses that may not be fully captured by numerical metrics alone.

The repository includes representative comparison panels and segmentation overlays generated during evaluation.

---

## Representative Comparison Panels

The comparison panels provide a side-by-side visual comparison of the two models for identical test images.

Each panel contains four components:

1. Original RGB image.
2. Ground-truth glass mask.
3. RGB prediction.
4. RGB-D prediction.

This arrangement enables direct visual comparison between the predicted segmentation masks and the corresponding ground-truth annotation. :contentReference[oaicite:4]{index=4}

The comparison panels show that both models successfully identify the principal glass regions within the scene. However, subtle differences in boundary localisation, prediction confidence, and the extent of the segmented glass area can be observed across individual examples.

These qualitative observations are consistent with the quantitative benchmark results, where the RGB model achieved slightly higher segmentation metrics.

---

## RGB Segmentation Overlays

The repository includes representative RGB overlay images in which the predicted glass regions are displayed directly on the original camera image.

Overlay visualisations make it easier to evaluate how well the segmentation output aligns with the physical glass surfaces within the scene.

The representative RGB overlay demonstrates that the model successfully identifies the majority of the annotated glass region while maintaining relatively accurate object boundaries. Minor false-positive regions are visible in some areas, but the principal glass surface is clearly recognised. :contentReference[oaicite:5]{index=5}

---

## RGB-D Segmentation Overlays

Equivalent overlay images are also provided for the early-fusion RGB-D model.

The representative RGB-D overlay shows successful localisation of the primary glass surface while exhibiting a slightly more conservative prediction in the illustrated example. In practical terms, this means that some portions of the labelled glass region remain unclassified, contributing to the slightly lower recall and Glass IoU observed during benchmark evaluation. :contentReference[oaicite:6]{index=6}

Although these differences are modest, they illustrate how qualitative evaluation complements benchmark metrics by revealing the spatial characteristics of the predicted segmentation masks.

---

## Qualitative Observations

Several consistent observations emerge from the qualitative evaluation.

- Both models successfully identify transparent glass across representative benchmark examples.
- The predicted segmentation masks closely follow the annotated glass regions.
- The RGB model generally produces more complete glass segmentation, particularly around object boundaries.
- The RGB-D model exhibits slightly more conservative predictions in some scenes, consistent with its lower recall and Glass IoU.
- Neither model demonstrates systematic failure across the representative qualitative examples provided in the repository.

The qualitative analysis therefore supports the conclusions drawn from the quantitative benchmark evaluation. Rather than contradicting the numerical results, the visual evidence provides additional confidence that the observed differences between the two models are genuine and reflect consistent segmentation behaviour across representative test images.

---

# 7. Deployment Results

While benchmark evaluation provides an objective assessment of segmentation accuracy, the ultimate objective of this study is to determine whether semantic glass detection can support safe mobile robot navigation.

To address this objective, the benchmark-selected RGB and early-fusion RGB-D models were deployed on a Pioneer P3-DX mobile robot equipped with a Microsoft Kinect camera. Both models were evaluated using the same deployment pipeline, hardware platform, navigation logic, and decision thresholds to ensure a fair comparison.

Unlike the benchmark experiments, which evaluate segmentation quality using static images, the deployment experiments assessed the behaviour of the complete perception system operating continuously during robot navigation.

The deployment results therefore complement the benchmark evaluation by demonstrating how semantic segmentation performance translates into practical robotic behaviour.

---

## Real-Time Semantic Segmentation

During deployment, both trained models successfully performed continuous semantic segmentation using live camera input from the Microsoft Kinect.

Each incoming frame passed through the complete deployment pipeline:

```text
Live Camera Frame
        │
        ▼
Image Pre-processing
        │
        ▼
SegFormer Inference
        │
        ▼
Binary Glass Mask
        │
        ▼
Center-Ratio Analysis
        │
        ▼
Navigation Decision
```

The generated segmentation masks were analysed in real time using the center-ratio decision rule described in the deployment documentation.

Successful execution of this pipeline demonstrated that transformer-based semantic segmentation could operate as part of a practical robotic perception system rather than solely as an offline benchmark model.

---

## Semantic Stopping Behaviour

The primary objective of the deployment experiments was to determine whether semantic perception could identify transparent glass before physical contact occurred.

For every incoming camera frame, the deployment software calculated the proportion of pixels classified as glass within the predefined decision region.

If the calculated center ratio exceeded the configured threshold, the robot immediately received a semantic stop command.

Otherwise, the robot continued navigating while processing subsequent camera frames.

This decision process enabled semantic perception to influence robot behaviour directly without modifying the trained segmentation network.

The deployment experiments confirmed that both models were capable of generating semantic glass-triggered stops before reaching the transparent obstacle when operating under the selected deployment configuration.

---

## Threshold Evaluation

To evaluate deployment robustness, multiple center-ratio thresholds were investigated during robot testing.

The evaluated thresholds were:

| Threshold | Behaviour |
|-----------|-----------|
| 0.30 | Highest sensitivity |
| 0.35 | Selected operating threshold |
| 0.40 | Increased confidence requirement |
| 0.60 | Most conservative decision |

The threshold of **0.35** provided the most effective balance between sensitivity and robustness.

At this operating threshold, both the RGB and RGB-D models generated semantic glass-triggered stops before physical contact with the glass partition while avoiding unnecessary interventions during non-glass trials.

Increasing the threshold required progressively stronger semantic evidence before issuing a stop command.

These observations demonstrate that deployment behaviour depends not only on segmentation accuracy but also on how segmentation outputs interact with the selected navigation decision rule.

---

## Comparative Deployment Performance

Although both models successfully supported semantic glass detection, differences emerged during practical deployment.

The RGB model consistently generated semantic stop commands throughout the evaluated threshold range.

The RGB-D model also successfully detected transparent glass at the selected operating threshold. However, at the stricter thresholds of **0.40** and **0.60**, the segmentation output occasionally produced insufficient semantic evidence to satisfy the decision rule before the robot approached the predefined safety distance.

In these situations, robot motion was terminated by the independent distance-based safety mechanism rather than by semantic perception.

These observations are consistent with the benchmark evaluation, where the RGB model achieved slightly higher recall and Glass IoU, producing more complete segmentation of transparent glass surfaces.

---

## Deployment Evidence

Representative deployment outputs are included within the repository to illustrate the behaviour of both deployment configurations.

The RGB deployment example demonstrates successful semantic perception using the trained RGB SegFormer model during live robot operation.

Likewise, the RGB-D deployment example illustrates semantic segmentation using the four-channel early-fusion model under the same deployment framework.

The representative terminal outputs provide visual evidence that both systems successfully integrated:

- live Kinect image acquisition;
- semantic segmentation inference;
- center-ratio analysis;
- navigation decision making;
- robot stopping behaviour.

These deployment examples demonstrate the successful integration of deep-learning perception with a physical mobile robotic platform. :contentReference[oaicite:1]{index=1}

---

# 8. Benchmark versus Deployment

One of the central objectives of this study was to investigate whether benchmark semantic segmentation performance accurately predicts practical robot behaviour.

The deployment experiments demonstrate that benchmark evaluation and real-world deployment should be viewed as complementary rather than interchangeable.

Benchmark testing provides objective, repeatable measurements of segmentation quality under controlled conditions.

Deployment evaluation, however, measures how those predictions influence the behaviour of a complete robotic system operating in real time.

The relationship between the two evaluation stages is summarised below.

| Benchmark Evaluation | Practical Deployment |
|----------------------|----------------------|
| Static benchmark images | Continuous live camera stream |
| Offline processing | Real-time inference |
| Numerical performance metrics | Robot behaviour |
| Segmentation quality | Navigation performance |
| Controlled evaluation | Dynamic operation |

Although both models achieved strong benchmark performance, practical deployment revealed additional considerations that cannot be measured using segmentation metrics alone.

These include:

- robustness to different decision thresholds;
- consistency of semantic stopping behaviour;
- interaction between perception and navigation;
- operational safety during robot movement.

Consequently, benchmark metrics should not be interpreted as the sole indicator of deployment performance.

Instead, practical robot evaluation provides an essential second stage of validation for perception systems intended for autonomous navigation.

---

## Lessons Learned

Several important lessons emerged from combining benchmark evaluation with practical deployment.

First, transformer-based semantic segmentation can successfully support transparent glass detection during mobile robot operation.

Second, relatively small benchmark performance differences can influence practical robot behaviour when segmentation outputs are incorporated into deterministic navigation decisions.

Third, semantic perception is most effective when integrated with conventional safety mechanisms rather than replacing them entirely.

Finally, the benchmark-to-robot evaluation methodology adopted in this project provides a more comprehensive assessment of perception systems than benchmark testing alone.

Together, the benchmark and deployment results demonstrate that the RGB SegFormer model provided the strongest overall combination of segmentation accuracy, inference efficiency, threshold robustness, and practical robotic performance under the experimental conditions evaluated in this study.

---

# 9. Limitations

The results presented in this study should be interpreted within the scope of the experimental design and deployment environment.

First, benchmark evaluation was conducted using a single public dataset, the RGB-D Glass Surface Detection (RGB-D GSD) dataset. Although this dataset provides a controlled benchmark for transparent glass segmentation, additional datasets containing a wider variety of glass types, lighting conditions, and environmental complexity would provide a more comprehensive assessment of model generalisation.

Second, practical deployment was performed using a single robotic platform consisting of a Pioneer P3-DX mobile robot equipped with a first-generation Microsoft Kinect camera. While this configuration provided an effective platform for evaluating semantic glass detection, the observed performance may differ when using alternative robots or depth sensing technologies.

Third, this work focused exclusively on binary semantic segmentation of transparent glass. Other transparent materials, reflective objects, and more complex scene semantics were beyond the scope of the present investigation.

Another limitation concerns the multimodal fusion strategy. Only an early-fusion RGB-D implementation was investigated. Although early fusion provides a straightforward mechanism for incorporating depth information, alternative fusion strategies—including intermediate fusion, late fusion, and attention-based multimodal architectures—may produce different performance characteristics.

Finally, the deployment experiments focused on evaluating semantic perception rather than complete autonomous navigation. The semantic segmentation models were integrated with a deterministic decision module and an independent distance-based safety mechanism, but the study did not attempt to evaluate full SLAM, path planning, localisation, or obstacle avoidance performance.

These limitations define the scope of the present work and should not be interpreted as shortcomings of the proposed methodology. Instead, they identify areas where future investigations can extend the benchmark-to-robot evaluation framework developed in this project. :contentReference[oaicite:1]{index=1}

---

# 10. Future Work

The findings of this study provide several opportunities for future research in semantic perception for mobile robotics.

One natural extension would be to evaluate the proposed benchmark-to-robot methodology using additional transparent-object datasets. Broader evaluation across multiple datasets would improve understanding of model robustness and generalisation under diverse environmental conditions.

Future work should also investigate alternative RGB-D sensing technologies. Modern depth cameras with improved accuracy and noise characteristics may provide more reliable geometric information for transparent object perception than the first-generation Kinect used in this study.

From a machine learning perspective, future research could compare early fusion with more advanced multimodal fusion strategies. Intermediate fusion, late fusion, cross-attention mechanisms, and confidence-aware depth integration may provide more effective utilisation of complementary RGB and depth information.

Additional opportunities include:

- evaluation under more challenging indoor environments;
- testing under varying illumination conditions;
- deployment on alternative mobile robotic platforms;
- optimisation for embedded and edge computing devices;
- incorporation of temporal information from consecutive video frames;
- investigation of uncertainty-aware semantic segmentation for safety-critical navigation.

Beyond perception, future work could integrate semantic glass detection into complete autonomous navigation systems incorporating simultaneous localisation and mapping (SLAM), path planning, obstacle avoidance, and long-term autonomous exploration.

These research directions would further strengthen the practical applicability of semantic perception for safe mobile robot navigation while building upon the controlled evaluation framework established in this project. :contentReference[oaicite:2]{index=2}

---

# 11. Results Summary

This document has presented a comprehensive evaluation of RGB and early-fusion RGB-D semantic segmentation models for transparent glass detection using both benchmark testing and practical robot deployment.

The benchmark evaluation demonstrated that both models achieved strong semantic segmentation performance across all reported evaluation metrics. However, the RGB model consistently produced slightly higher Pixel Accuracy, Mean Intersection over Union, Glass IoU, Precision, Recall, and F1-score on the held-out benchmark dataset.

Qualitative evaluation supported these findings by showing that both models successfully identified transparent glass regions while the RGB model generally produced more complete and consistent segmentations across representative benchmark examples.

Practical deployment on the Pioneer P3-DX mobile robot confirmed that benchmark segmentation models could be successfully integrated into a real-time robotic perception pipeline. Both models supported semantic glass detection during robot operation, while the RGB model demonstrated greater robustness across the evaluated decision thresholds.

Taken together, the benchmark and deployment experiments demonstrate that offline segmentation metrics provide valuable insight into model performance but do not fully characterise practical robotic behaviour. Evaluating perception systems within complete robotic platforms reveals additional considerations—including inference efficiency, threshold robustness, and semantic stopping consistency—that are not captured by benchmark metrics alone.

Within the scope of the evaluated dataset, hardware platform, and deployment methodology, the RGB SegFormer-B0 model provided the strongest overall balance of segmentation accuracy, computational efficiency, and practical deployment performance. The benchmark-to-robot evaluation framework adopted throughout this project therefore offers a comprehensive approach for assessing semantic perception systems intended for safe mobile robot navigation.

---

## Key Takeaways

The principal findings of this project can be summarised as follows:

- Both RGB and early-fusion RGB-D SegFormer-B0 models achieved strong transparent glass segmentation performance.
- The RGB model consistently outperformed the RGB-D model across all reported benchmark metrics.
- Successful deployment demonstrated that transformer-based semantic segmentation can support real-time transparent glass detection on a mobile robotic platform.
- Benchmark evaluation and practical deployment provide complementary perspectives on perception performance and should be considered together when evaluating robotic vision systems.
- The benchmark-to-robot methodology developed in this project provides a reproducible framework for future research in semantic perception for autonomous mobile robots.