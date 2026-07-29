#!/usr/bin/env bash
set -euo pipefail

python -m src.evaluate \
  --checkpoint outputs/rgb_segformer/best_model.pt \
  --config configs/rgb.yaml \
  --split test

python -m src.evaluate \
  --checkpoint outputs/rgbd_segformer/best_model.pt \
  --config configs/rgbd.yaml \
  --split test
