# Running the Experiments

## Train the RGB Model

Shell script:

```bash
bash scripts/train_rgb.sh
```

Equivalent Python command:

```bash
python -m src.train --config configs/rgb.yaml
```

## Train the RGB-D Model

Shell script:

```bash
bash scripts/train_rgbd.sh
```

Equivalent Python command:

```bash
python -m src.train --config configs/rgbd.yaml
```

## Evaluate Both Models

```bash
bash scripts/evaluate.sh
```

The evaluation script runs the RGB and RGB-D benchmark evaluations using their respective configuration files and selected checkpoints.

## Expected Outputs

Training and evaluation produce:

- configuration snapshots
- training histories
- validation results
- held-out test metrics
- selected checkpoints
- qualitative predictions where enabled

Experiment summaries are stored under `outputs/` and `results/`.

## Generate Comparison Panels

Use the supplied comparison-panel utility:

```bash
python scripts/make_comparison_panels.py
```

The generated panels are stored in:

```text
results/comparison_panels/
```

## Reproduction Sequence

1. Install the dependencies.
2. Prepare the RGB-D GSD dataset.
3. Verify dataset paths in both YAML configurations.
4. Train the RGB model.
5. Train the RGB-D model.
6. Evaluate both selected checkpoints on the test split.
7. Generate qualitative outputs and comparison panels.
8. Review the metrics in `outputs/` and the visual evidence in `results/`.
9. Run live deployment only when the required Pioneer P3-DX and Kinect hardware are available.
