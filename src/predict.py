from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from src.models.segformer_rgbd import build_segformer
from src.utils.config import load_config
from src.utils.visualization import save_mask_overlay


def load_rgb(path: str | Path, image_size: int) -> np.ndarray:
    image = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_LINEAR)
    return image


def load_depth(path: str | Path, image_size: int, depth_max_value: float | None = None) -> np.ndarray:
    path = Path(path)
    if path.suffix.lower() == ".npy":
        depth = np.load(path).astype(np.float32)
    else:
        depth = np.asarray(Image.open(path), dtype=np.float32)
    if depth.ndim == 3:
        depth = depth[..., 0]

    depth = np.where(np.isfinite(depth), depth, 0.0)
    if depth_max_value is not None:
        depth = np.clip(depth, 0.0, float(depth_max_value)) / float(depth_max_value)
    else:
        valid = depth[depth > 0]
        if valid.size > 0:
            low, high = np.percentile(valid, [1, 99])
            if high > low:
                depth = np.clip(depth, low, high)
                depth = (depth - low) / (high - low)
            else:
                depth = np.zeros_like(depth, dtype=np.float32)
        else:
            depth = np.zeros_like(depth, dtype=np.float32)

    depth = cv2.resize(depth.astype(np.float32), (image_size, image_size), interpolation=cv2.INTER_LINEAR)
    return depth


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict glass segmentation mask using trained SegFormer")
    parser.add_argument("--checkpoint", required=True, help="Path to checkpoint .pt file")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--rgb", required=True, help="Path to RGB image")
    parser.add_argument("--depth", default=None, help="Path to depth image or .npy file for RGB-D mode")
    parser.add_argument("--output", required=True, help="Path to save overlay image")
    parser.add_argument("--mask-output", default=None, help="Optional path to save raw predicted mask")
    args = parser.parse_args()

    cfg = load_config(args.config)
    modality = cfg["modality"].lower()
    image_size = int(cfg["image_size"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    rgb = load_rgb(args.rgb, image_size)
    if modality == "rgbd":
        if args.depth is None:
            raise ValueError("--depth is required when config modality is rgbd")
        depth = load_depth(args.depth, image_size, cfg.get("depth_max_value"))
        image = np.concatenate([rgb, depth[..., None]], axis=-1)
    else:
        image = rgb

    mean = np.array(cfg["mean"], dtype=np.float32).reshape(1, 1, -1)
    std = np.array(cfg["std"], dtype=np.float32).reshape(1, 1, -1)
    image = (image - mean) / std

    pixel_values = torch.from_numpy(image.transpose(2, 0, 1)).float().unsqueeze(0).to(device)
    in_channels = 4 if modality == "rgbd" else 3

    model = build_segformer(
        model_name=cfg.get("model_name", "nvidia/mit-b0"),
        num_classes=int(cfg["num_classes"]),
        in_channels=in_channels,
        ignore_index=int(cfg.get("ignore_index", 255)),
        pretrained=bool(cfg.get("pretrained", True)),
    ).to(device)

    checkpoint = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    model.eval()

    with torch.no_grad():
        outputs = model(pixel_values=pixel_values)
        logits = F.interpolate(outputs.logits, size=(image_size, image_size), mode="bilinear", align_corners=False)
        pred = torch.argmax(logits, dim=1)[0].cpu().numpy().astype(np.uint8)

    save_mask_overlay(args.rgb, pred, args.output, glass_class_id=int(cfg.get("glass_class_id", 1)))
    print(f"Saved overlay to: {args.output}")

    if args.mask_output:
        mask_output = Path(args.mask_output)
        mask_output.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(pred).save(mask_output)
        print(f"Saved raw mask to: {mask_output}")


if __name__ == "__main__":
    main()
