#!/usr/bin/env bash
set -euo pipefail
python -m src.train --config configs/rgbd.yaml
