# Deployment

## 1. Introduction

This document describes the deployment of the trained RGB and early-fusion RGB-D semantic segmentation models on a Pioneer P3-DX mobile robot. The objective of the deployment stage is to evaluate whether benchmark segmentation performance translates into reliable real-time glass detection during autonomous robot operation.

While benchmark datasets provide an objective means of comparing segmentation accuracy, they cannot fully represent the conditions encountered during practical robot navigation. Real-world deployment introduces additional challenges including continuous image acquisition, inference latency, communication delays, environmental variation, and interaction with robot control systems.

To address this gap, the trained models were integrated into a complete perception pipeline consisting of live image acquisition, semantic segmentation, decision making, and robot motion control. The deployment framework enables transparent glass to be detected in real time and allows semantic perception to influence robot navigation behaviour.

Unlike the benchmark evaluation, which focuses primarily on segmentation quality, the deployment experiments assess how effectively each model supports safe robot operation when processing continuous camera input.

The deployment methodology follows the benchmark-to-robot evaluation strategy presented in the accompanying research paper, using identical trained checkpoints for both RGB and RGB-D models without any additional fine-tuning before deployment. :contentReference[oaicite:1]{index=1}

---

## 2. Deployment Objectives

The deployment stage was designed to answer several practical questions that cannot be addressed using benchmark metrics alone.

The primary objectives were:

- determine whether the trained segmentation models operate reliably during continuous robot navigation;
- evaluate whether transparent glass can be detected before physical contact;
- compare RGB and RGB-D behaviour under identical deployment conditions;
- measure the consistency of semantic stopping behaviour;
- investigate the relationship between benchmark performance and real-world navigation performance.

Rather than replacing conventional obstacle avoidance, semantic glass detection operates as an additional perception capability capable of recognising transparent obstacles that may not be reliably identified by standard navigation sensors.

The deployment experiments therefore complement the benchmark evaluation by examining operational performance instead of only numerical segmentation accuracy.

---

## 3. Hardware Platform

Practical deployment was performed using the same hardware platform described in the accompanying paper.

The deployment system consisted of:

| Component | Description |
|------------|-------------|
| Mobile Robot | Pioneer P3-DX |
| Camera | Microsoft Kinect for Windows (First Generation) |
| Processing Computer | ASUS Vivobook 16X |
| Processor | Intel Core i7-13700H |
| Memory | 16 GB RAM |
| GPU | NVIDIA GeForce RTX 4050 Laptop GPU (6 GB) |

The Pioneer P3-DX serves as the mobile robotic platform responsible for executing navigation commands.

Image acquisition is performed using a first-generation Microsoft Kinect camera mounted on the robot. Although the Kinect provides both RGB and depth data, the deployment experiments use the same trained models produced during benchmark evaluation without modifying their learned parameters.

All neural network inference is performed on the external laptop GPU rather than onboard the robot. This configuration allows transformer inference to execute efficiently while preserving the robot's existing control framework. :contentReference[oaicite:2]{index=2}

---

## 4. Software Architecture

The deployment software is organised into several independent components that communicate sequentially throughout the perception pipeline.

The principal software modules include:

- camera interface;
- image preprocessing;
- SegFormer inference;
- semantic mask generation;
- decision logic;
- robot communication;
- motion control.

Separating these functions into modular components simplifies debugging, maintenance, and future system extension while allowing each stage of the perception pipeline to be evaluated independently.

The trained RGB and RGB-D checkpoints are loaded dynamically depending on the selected deployment configuration.

No architectural modifications are introduced during deployment. The same checkpoints obtained following benchmark evaluation are used directly during practical robot testing.

---

## 5. Overall Deployment Pipeline

The deployment pipeline transforms live camera images into navigation decisions through a sequence of perception and decision-making stages.

The complete workflow is illustrated below.

```text
Microsoft Kinect Camera
          │
          ▼
Image Acquisition
          │
          ▼
Image Pre-processing
          │
          ▼
SegFormer Inference
          │
          ▼
Semantic Glass Mask
          │
          ▼
Center-Ratio Analysis
          │
          ▼
Decision Logic
          │
          ▼
Robot Command
          │
          ▼
Continue or Stop
```

Each stage executes sequentially for every incoming camera frame. The generated segmentation mask is analysed to determine whether sufficient evidence of transparent glass exists within the predefined decision region. If the configured threshold is exceeded, a semantic stop command is transmitted to the robot. Otherwise, normal navigation continues.

This perception pipeline enables semantic understanding of transparent obstacles to be incorporated into the robot's navigation process while preserving an independent distance-based safety mechanism as the final layer of protection. :contentReference[oaicite:3]{index=3}

---

# 6. Model Deployment Pipeline

The deployment pipeline converts live camera observations into navigation decisions through a sequence of image acquisition, preprocessing, semantic segmentation, and decision-making stages. Each stage executes sequentially for every incoming frame captured by the Microsoft Kinect camera.

Unlike the benchmark experiments, where images are processed offline, deployment operates continuously while the robot navigates through an indoor environment. The objective is to determine whether the trained semantic segmentation models can provide sufficiently reliable glass detection to influence robot behaviour in real time.

Both the RGB and RGB-D deployment pipelines follow the same processing sequence. The only difference is the model input, where the RGB model receives a three-channel colour image and the RGB-D model receives an aligned four-channel RGB-D image.

The deployment workflow is illustrated below.

```text
Camera Capture
      │
      ▼
Frame Acquisition
      │
      ▼
Image Pre-processing
      │
      ▼
SegFormer Model
      │
      ▼
Semantic Segmentation Mask
      │
      ▼
Center-Ratio Analysis
      │
      ▼
Decision Logic
      │
      ▼
Motion Command
```

Maintaining an identical deployment pipeline for both models ensures that any differences in robot behaviour arise from the perception model rather than differences in the surrounding software architecture.

---

# 7. Camera Image Acquisition

Visual information is obtained using a first-generation Microsoft Kinect for Windows camera mounted on the Pioneer P3-DX mobile robot.

The Kinect provides synchronised RGB and depth streams, enabling both deployment configurations to operate under identical environmental conditions. During deployment, camera frames are acquired continuously and forwarded to the inference computer for processing.

The RGB deployment uses only the colour stream, while the RGB-D deployment combines the colour image with its corresponding aligned depth image before inference.

The camera position is fixed throughout all deployment experiments to maintain a consistent field of view. This ensures that both models observe identical scenes during comparative evaluation.

Frame acquisition continues throughout robot motion until either a semantic stop or the independent distance-based safety stop terminates the run. :contentReference[oaicite:2]{index=2}

---

# 8. Image Pre-processing

Before inference, each captured frame undergoes preprocessing to match the format used during model training.

The preprocessing pipeline includes:

- acquisition of the current RGB image;
- acquisition of the aligned depth image (RGB-D configuration only);
- resizing to the network input resolution;
- normalisation of image values;
- conversion to tensor format.

Maintaining identical preprocessing during training and deployment reduces domain mismatch and helps preserve model performance under real operating conditions.

For RGB deployment, the processed input consists of a three-channel image.

For RGB-D deployment, the normalised depth image is concatenated with the RGB image to produce a four-channel tensor before being passed to the network.

No additional filtering or enhancement is applied during deployment, ensuring that the models are evaluated using live sensor data under realistic operating conditions.

---

# 9. SegFormer Inference

Once preprocessing is complete, the prepared input tensor is passed to the trained SegFormer-B0 model for semantic segmentation.

Inference is performed using the frozen checkpoint selected during benchmark evaluation. No additional training, fine-tuning, or parameter updates occur during deployment.

Depending on the selected configuration, the deployment software loads either:

- the RGB SegFormer-B0 checkpoint; or
- the early-fusion RGB-D SegFormer-B0 checkpoint.

The network predicts a pixel-wise semantic segmentation mask in which each pixel is classified as either:

| Class | Meaning |
|---------|---------|
| Background | Non-glass surface |
| Glass | Transparent glass surface |

The inference stage represents the computational core of the deployment pipeline and directly influences the subsequent navigation decision.

Using identical frozen checkpoints throughout deployment ensures consistency with the benchmark evaluation and allows deployment behaviour to be interpreted in the context of the reported benchmark metrics. :contentReference[oaicite:3]{index=3}

---

# 10. Segmentation Mask Generation

The output of the segmentation network is converted into a binary semantic mask representing the predicted glass regions within the current camera frame.

Each pixel in the generated mask is assigned one of two semantic labels:

- background; or
- glass.

The binary mask provides the semantic representation used by the navigation decision module. Rather than analysing the entire image uniformly, subsequent processing focuses on a predefined decision region corresponding to the robot's forward direction.

A representative processing sequence is shown below.

```text
RGB / RGB-D Image
        │
        ▼
SegFormer Prediction
        │
        ▼
Probability Map
        │
        ▼
Binary Glass Mask
        │
        ▼
Decision Region Extraction
```

This intermediate representation separates semantic perception from robot control, allowing the decision logic to operate independently of the segmentation network itself.

---

# 11. Post-processing

Following segmentation, the predicted mask is prepared for navigation analysis.

The deployment software extracts the predefined decision region from the binary segmentation mask and computes the proportion of pixels classified as glass within that region.

No morphological filtering, temporal smoothing, or frame averaging is applied before the decision stage. This design allows the deployment experiments to evaluate the segmentation models directly without introducing additional post-processing algorithms that could influence the comparative results.

Maintaining a minimal post-processing pipeline preserves the controlled nature of the study and ensures that observed differences between the RGB and RGB-D deployments originate from the perception models themselves rather than subsequent processing steps.

The processed decision region is then forwarded to the semantic decision module, where the center-ratio threshold is evaluated to determine whether a semantic stop command should be issued to the Pioneer P3-DX.

---

# 12. Semantic Safety Layer

The semantic safety layer provides the interface between the segmentation model and the robot navigation system. Rather than directly controlling robot motion, the segmentation model supplies semantic information indicating the presence or absence of transparent glass within the robot's field of view.

This semantic information is analysed by a deterministic decision module that determines whether sufficient evidence exists to issue a glass-triggered stop command.

Separating semantic perception from motion control provides several advantages:

- the segmentation model remains independent of robot navigation software;
- decision logic can be modified without retraining the network;
- deployment behaviour remains transparent and reproducible;
- semantic detection can be combined with conventional safety mechanisms.

The semantic safety layer therefore functions as an additional perception capability rather than a replacement for traditional obstacle avoidance.

The complete decision process is illustrated below.

```text
Camera Frame
      │
      ▼
SegFormer Prediction
      │
      ▼
Binary Glass Mask
      │
      ▼
Decision Region Analysis
      │
      ▼
Center-Ratio Calculation
      │
      ▼
Threshold Comparison
      │
      ├───────────────┐
      │               │
      ▼               ▼
Continue          Stop Robot
```

This modular design enables semantic perception and robot control to remain logically separated while supporting consistent deployment behaviour.

---

# 13. Center-Ratio Decision Rule

Robot stopping decisions are based on a simple geometric measurement referred to as the **center ratio**.

Rather than analysing the entire segmentation mask, the deployment system evaluates only the central portion of the predicted image corresponding to the robot's forward path.

As described in the accompanying paper, the decision region is defined as the **full-height central third of the predicted segmentation mask**. The numerator is the number of pixels classified as glass within this region, while the denominator is the total number of pixels contained within the same region. :contentReference[oaicite:2]{index=2}

The center ratio therefore represents the proportion of the robot's forward viewing region that is predicted to contain transparent glass.

Conceptually, the calculation can be represented as:

```text
Predicted Segmentation Mask

┌──────────────────────────────┐
│                              │
│          │██████│            │
│          │██████│            │
│          │██████│            │
│          │██████│            │
│          │██████│            │
│                              │
└──────────────────────────────┘

Decision Region = Center Third

Center Ratio =
Glass Pixels inside Region
──────────────────────────
Total Pixels in Region
```

A larger center ratio indicates stronger evidence that a transparent obstacle occupies the robot's intended direction of travel.

This approach provides a simple, deterministic mechanism for converting dense semantic segmentation into an actionable navigation decision while remaining computationally efficient.

---

# 14. Threshold Selection

The calculated center ratio is compared with a predefined decision threshold.

If the calculated value equals or exceeds the configured threshold, a semantic stop command is generated. Otherwise, the robot continues moving normally.

During deployment, four threshold values were evaluated:

| Threshold | Purpose |
|-----------|---------|
| 0.30 | Sensitivity evaluation |
| 0.35 | Selected operating threshold |
| 0.40 | Increased detection confidence |
| 0.60 | Conservative stopping evaluation |

The threshold of **0.35** was selected as the operational configuration because both models consistently generated glass-triggered stops while maintaining a practical stopping distance before contact with the glass partition. :contentReference[oaicite:3]{index=3}

Evaluating multiple thresholds provided additional insight into deployment robustness by demonstrating how each model responded under increasingly strict decision criteria.

This threshold sweep complements benchmark evaluation by revealing behaviour that cannot be inferred from segmentation metrics alone.

---

# 15. Robot Communication

Once a navigation decision has been made, the deployment software communicates the corresponding command to the Pioneer P3-DX control framework.

The communication stage receives one of two possible outcomes from the decision module:

- continue navigation; or
- issue a semantic stop.

The inference process executes on the external evaluation laptop, while motion commands are transmitted to the robot through the existing control framework. This architecture allows the perception system to operate independently of the low-level robot controller while maintaining reliable communication between perception and navigation. :contentReference[oaicite:4]{index=4}

Maintaining this separation simplifies deployment and allows alternative perception models to be integrated without modifying the robot's underlying motion control software.

---

# 16. Motion Commands

Following communication with the robot controller, the Pioneer P3-DX executes the corresponding navigation action.

Two possible behaviours are supported:

### Continue Navigation

If the calculated center ratio remains below the configured threshold, the deployment software does not generate a semantic intervention.

The robot therefore continues normal forward navigation while continuously acquiring and analysing new camera frames.

### Semantic Stop

If the center ratio equals or exceeds the configured threshold, the deployment software immediately issues a semantic stop command.

The robot terminates forward motion before reaching the detected glass surface.

This behaviour allows transparent obstacles to be recognised using semantic perception rather than relying solely on conventional range sensing.

The complete decision sequence is summarised below.

```text
Camera Frame

↓

SegFormer Prediction

↓

Center-Ratio Calculation

↓

Threshold Comparison

↓

Center Ratio ≥ Threshold ?

        │
   ┌────┴────┐
   │         │
 No         Yes
   │         │
Continue   Stop Robot
```

---

# 17. Independent Distance-Based Safety Layer

Although semantic segmentation provides the primary mechanism for glass detection, deployment retains an independent distance-based safety stop throughout every experiment.

This safety mechanism operates separately from the semantic perception pipeline and remains active regardless of the segmentation model being evaluated.

If the semantic system does not issue a glass-triggered stop before the robot reaches the minimum safe distance, the distance-based safety mechanism terminates robot motion.

Maintaining this independent safety layer ensures that deployment remains safe even if semantic segmentation fails to detect a transparent obstacle.

As reported in the accompanying paper, the fallback safety mechanism successfully prevented contact during the RGB-D runs in which the stricter thresholds were not reached before the robot approached the glass partition. :contentReference[oaicite:5]{index=5}

This layered approach reflects a practical safety philosophy in which semantic perception extends environmental awareness while deterministic proximity protection remains the final safeguard against collision.

---

# 18. Experimental Procedure

Following benchmark evaluation, the selected RGB and RGB-D checkpoints were deployed without modification on the Pioneer P3-DX mobile robot. The objective of the deployment experiments was to determine whether benchmark segmentation performance translated into reliable semantic glass detection during practical robot operation.

Both models were evaluated using the same deployment pipeline, hardware platform, camera, laboratory environment, navigation logic, and stopping criteria. Maintaining identical deployment conditions ensured that differences in robot behaviour could be attributed to the segmentation models rather than variations in the experimental setup.

Each deployment trial followed the same sequence:

1. Load the selected trained model.
2. Initialise the Kinect camera.
3. Establish communication with the Pioneer P3-DX.
4. Begin continuous image acquisition.
5. Perform real-time semantic segmentation.
6. Calculate the center ratio for each frame.
7. Compare the calculated value with the configured threshold.
8. Continue navigation or issue a semantic stop.
9. Record the outcome of the trial.

This procedure was repeated for both deployment configurations under the same operating conditions.

---

# 19. Deployment Evaluation Protocol

The deployment experiments were designed to evaluate semantic stopping behaviour rather than navigation performance alone.

The robot approached either a transparent glass partition or a non-glass scene while continuously processing camera images using the selected segmentation model.

For every captured frame, the deployment software generated:

- a semantic segmentation mask;
- a center-ratio measurement;
- a navigation decision.

Each deployment run terminated in one of two ways:

- a semantic glass-triggered stop; or
- an independent distance-based safety stop.

The deployment protocol therefore distinguished successful semantic perception from fallback protection.

Unlike benchmark evaluation, where segmentation quality is measured numerically, deployment evaluation focused on whether semantic perception produced the intended robot behaviour under realistic operating conditions.

---

# 20. Threshold Evaluation

To investigate deployment robustness, multiple decision thresholds were evaluated.

The recorded experiments considered the following center-ratio thresholds:

| Threshold | Evaluation Purpose |
|-----------|--------------------|
| 0.30 | Low decision threshold |
| 0.35 | Selected operating threshold |
| 0.40 | Increased confidence threshold |
| 0.60 | Conservative decision threshold |

Evaluating multiple thresholds provides insight into how each segmentation model behaves under different decision sensitivities.

Lower thresholds increase the likelihood of semantic intervention, whereas higher thresholds require stronger evidence before issuing a stop command.

As reported in the accompanying paper, the threshold of **0.35** was selected because both models produced glass-triggered stops after a practical approach distance while avoiding false semantic interventions in non-glass scenes. :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}

The threshold sweep also demonstrated that models with similar benchmark metrics may behave differently when integrated into a deterministic navigation rule.

---

# 21. Trial Recording

Each deployment run was documented using both quantitative measurements and qualitative observations.

The recorded information included:

- deployment configuration;
- selected threshold;
- scene type;
- stopping mechanism;
- distance travelled;
- runtime.

For glass scenes, the experiments recorded whether the semantic perception system generated a glass-triggered stop before the independent distance-based safety mechanism intervened.

For non-glass scenes, the experiments confirmed that no unnecessary semantic stop commands were generated.

This recording procedure enabled direct comparison between benchmark segmentation performance and practical deployment behaviour.

---

# 22. Practical Observations

The deployment experiments demonstrated that both trained models were capable of performing real-time semantic segmentation during robot navigation.

At the selected operating threshold of **0.35**, both the RGB and RGB-D models successfully generated semantic glass-triggered stops during the recorded glass trials before physical contact with the glass partition occurred. :contentReference[oaicite:3]{index=3}

However, increasing the decision threshold revealed differences between the two models.

The RGB model continued to generate semantic glass-triggered stops across all recorded glass runs, whereas the RGB-D model relied on the independent distance-based safety mechanism during the stricter threshold evaluations. :contentReference[oaicite:4]{index=4}

No false semantic glass detections were observed during the recorded non-glass deployment runs.

These observations illustrate that benchmark metrics alone do not fully describe deployment behaviour. Small differences in segmentation quality may influence the spatial evidence delivered to the navigation decision module and therefore affect the resulting robot actions.

---

# 23. Integration Considerations

Deploying deep-learning perception on a mobile robot requires more than accurate semantic segmentation.

The deployment experiments highlighted the importance of integrating perception, decision making, and robot control into a coherent processing pipeline.

Several practical considerations were observed during deployment:

- continuous camera acquisition;
- stable real-time inference;
- reliable communication between the perception computer and robot controller;
- deterministic decision logic;
- preservation of an independent safety mechanism.

The accompanying paper also notes intermittent frame-read conflicts associated with the file-based Kinect bridge. These events were transient and did not alter the recorded deployment outcomes, indicating that they were integration artefacts rather than evidence of segmentation failure. :contentReference[oaicite:5]{index=5}

These observations reinforce the importance of evaluating perception systems within complete robotic platforms rather than relying exclusively on benchmark datasets.

---

# 24. Failure Handling

The deployment framework was intentionally designed to tolerate situations in which semantic perception alone was insufficient to prevent collision.

If the segmentation model failed to generate a glass-triggered stop before the robot reached the predefined safety distance, the independent distance-based safety mechanism immediately terminated robot motion.

This layered safety strategy ensured that every deployment trial concluded safely, regardless of whether the semantic trigger or the fallback protection mechanism initiated the stop.

Maintaining an independent deterministic safety layer reflects practical robotic system design, where learned perception complements—but does not replace—conventional collision avoidance mechanisms.

The deployment experiments therefore evaluate semantic perception as an enhancement to robot safety rather than as the sole protective mechanism.

---

# 25. Deployment Results

The deployment experiments demonstrated that both trained models were capable of supporting real-time semantic glass detection during practical robot operation. The deployment stage confirmed that benchmark semantic segmentation models could be successfully integrated into a mobile robotic perception pipeline without additional training or architectural modification.

At the selected operating threshold of **0.35**, both the RGB and early-fusion RGB-D models generated semantic glass-triggered stops during the recorded glass trials before physical contact with the transparent obstacle occurred. Neither model produced false semantic glass detections during the recorded non-glass trials, indicating that the deployed perception system remained selective under the evaluated laboratory conditions. :contentReference[oaicite:1]{index=1}

When evaluated across the complete threshold sweep, differences between the two models became more apparent. The RGB model consistently generated semantic glass-triggered stops across all recorded glass runs, whereas the RGB-D model relied on the independent distance-based safety mechanism at the stricter thresholds of **0.40** and **0.60**. These observations were consistent with the benchmark evaluation, where the RGB model achieved higher recall, higher Glass IoU, lower inference latency, and greater throughput. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

The deployment experiments therefore demonstrated that relatively small differences observed during benchmark evaluation translated into measurable differences in robot behaviour when segmentation predictions were incorporated into a deterministic navigation rule.

---

# 26. Benchmark-to-Robot Translation

One of the principal objectives of this work was to determine whether benchmark semantic segmentation performance provides a reliable indication of practical robotic performance.

The deployment results show that benchmark metrics alone are insufficient to characterise operational behaviour. Although both models achieved strong segmentation performance on the held-out benchmark dataset, differences in recall, Glass IoU, inference latency, and threshold robustness influenced the frequency with which semantic stopping behaviour was successfully activated during robot operation.

The threshold evaluation demonstrated that models with relatively similar benchmark scores may produce different navigation outcomes when integrated into a complete perception and decision-making pipeline.

Consequently, practical deployment should be considered an essential complement to benchmark evaluation when assessing perception systems intended for autonomous mobile robots.

---

# 27. Reproducibility

The deployment framework has been designed to maximise experimental reproducibility.

The repository provides the principal resources required to reproduce the deployment workflow, including:

- deployment source code;
- trained RGB checkpoint;
- trained RGB-D checkpoint;
- configuration files;
- deployment documentation;
- representative terminal outputs;
- qualitative deployment evidence;
- benchmark evaluation results.

To reproduce the deployment experiments, users should:

1. Prepare the deployment hardware.
2. Configure the software environment.
3. Load one of the trained checkpoints.
4. Initialise the Kinect camera.
5. Establish communication with the Pioneer P3-DX.
6. Execute the deployment script.
7. Monitor the generated segmentation masks and navigation decisions.
8. Record semantic stopping behaviour.

Although hardware availability may differ between laboratories, the repository has been organised so that the deployment pipeline can be understood, reproduced, and adapted to similar robotic platforms.

---

# 28. Deployment Limitations

The deployment experiments should be interpreted within the scope of the evaluated system.

Several limitations should be acknowledged.

First, deployment was conducted using a Pioneer P3-DX mobile robot equipped with a first-generation Microsoft Kinect camera. Different robotic platforms or sensing hardware may produce different operational characteristics.

Second, the evaluation was performed within controlled indoor laboratory environments containing representative transparent glass obstacles. Additional evaluation across larger and more diverse environments would further strengthen the generalisability of the findings.

Third, only the trained RGB and early-fusion RGB-D SegFormer-B0 models were evaluated. Alternative multimodal fusion strategies, confidence-aware depth processing, or modality-specific encoder architectures may exhibit different deployment behaviour.

Finally, the semantic perception system operates alongside an independent distance-based safety mechanism. The deployment framework therefore evaluates semantic perception as an enhancement to robot safety rather than as a complete replacement for conventional collision avoidance.

These limitations are consistent with the scope of the accompanying research paper and provide opportunities for future investigation. :contentReference[oaicite:4]{index=4}

---

# 29. Future Improvements

The deployment framework provides a foundation for future research into semantic perception for safe mobile robot navigation.

Potential areas for future development include:

- evaluation using more recent RGB-D sensing hardware;
- investigation of intermediate and late-fusion architectures;
- confidence-aware depth representations;
- integration of temporal information across consecutive frames;
- deployment on additional robotic platforms;
- evaluation in larger and more complex indoor environments;
- incorporation of semantic perception into higher-level navigation and path-planning systems.

These directions would enable further investigation of transparent obstacle perception while maintaining the controlled experimental philosophy established in this study.

---

# 30. Deployment Summary

This document has described the practical deployment of RGB and early-fusion RGB-D semantic segmentation models on a Pioneer P3-DX mobile robot.

Beginning with live image acquisition from a Microsoft Kinect camera, the deployment pipeline performs image preprocessing, transformer-based semantic segmentation, binary mask generation, center-ratio analysis, deterministic decision making, and robot motion control. The semantic perception system operates alongside an independent distance-based safety mechanism to provide an additional layer of transparent obstacle awareness.

The deployment experiments demonstrate that benchmark evaluation alone does not fully characterise operational behaviour. Integrating semantic segmentation into a complete robotic perception pipeline reveals additional considerations, including threshold robustness, inference latency, and the consistency of semantic stopping behaviour.

Together with the benchmark evaluation presented in the accompanying paper, the deployment results support the conclusion that, for the evaluated SegFormer-B0 architecture and deployment configuration, the RGB model provided the most reliable balance of segmentation performance, computational efficiency, and practical robotic behaviour under controlled experimental conditions. :contentReference[oaicite:5]{index=5}