import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import torch
import numpy as np
from src.models.segformer_rgbd import build_segformer
from src.utils.config import load_config

checkpoint_path = "outputs/RGBD_001/best_model.pt"
config_path = "configs/rgbd.yaml"

cfg = load_config(config_path)

model = build_segformer(
    model_name=cfg.get("model_name", "nvidia/mit-b0"),
    num_classes=int(cfg["num_classes"]),
    in_channels=4,
    ignore_index=int(cfg.get("ignore_index", 255)),
    pretrained=bool(cfg.get("pretrained", True)),
)

checkpoint = torch.load(checkpoint_path, map_location="cpu")
model.load_state_dict(checkpoint["model_state_dict"], strict=True)

first_conv = None
first_name = None

for name, module in model.named_modules():
    if isinstance(module, torch.nn.Conv2d) and module.in_channels == 4:
        first_conv = module
        first_name = name
        break

if first_conv is None:
    raise RuntimeError("Could not find RGB-D first convolution.")

weights = first_conv.weight.detach().cpu().numpy()

# Shape: [out_channels, in_channels, kernel_h, kernel_w]
channel_weights = weights.reshape(weights.shape[0], weights.shape[1], -1)

channel_l1 = np.mean(np.abs(channel_weights), axis=(0, 2))
channel_l2 = np.sqrt(np.mean(channel_weights ** 2, axis=(0, 2)))

total_l1 = channel_l1.sum()
total_l2 = channel_l2.sum()

print("First RGB-D convolution:", first_name)
print("Weight shape:", weights.shape)

print("\nMean absolute weight per input channel (L1):")
print(f"R:     {channel_l1[0]:.6f}  ({channel_l1[0] / total_l1 * 100:.2f}%)")
print(f"G:     {channel_l1[1]:.6f}  ({channel_l1[1] / total_l1 * 100:.2f}%)")
print(f"B:     {channel_l1[2]:.6f}  ({channel_l1[2] / total_l1 * 100:.2f}%)")
print(f"Depth: {channel_l1[3]:.6f}  ({channel_l1[3] / total_l1 * 100:.2f}%)")

print("\nRoot mean square weight per input channel (L2):")
print(f"R:     {channel_l2[0]:.6f}  ({channel_l2[0] / total_l2 * 100:.2f}%)")
print(f"G:     {channel_l2[1]:.6f}  ({channel_l2[1] / total_l2 * 100:.2f}%)")
print(f"B:     {channel_l2[2]:.6f}  ({channel_l2[2] / total_l2 * 100:.2f}%)")
print(f"Depth: {channel_l2[3]:.6f}  ({channel_l2[3] / total_l2 * 100:.2f}%)")

rgb_mean_l1 = channel_l1[:3].mean()
depth_ratio_l1 = channel_l1[3] / rgb_mean_l1

print("\nDepth-to-average-RGB ratio:")
print(f"L1 ratio: {depth_ratio_l1:.4f}")

if depth_ratio_l1 < 0.5:
    print("\nInterpretation: Depth channel appears weakly used.")
elif depth_ratio_l1 > 1.5:
    print("\nInterpretation: Depth channel appears strongly weighted.")
else:
    print("\nInterpretation: Depth channel is weighted comparably to RGB channels.")