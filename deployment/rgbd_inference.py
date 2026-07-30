import sys
from pathlib import Path
import argparse
import time

import numpy as np
import torch
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.segformer_rgbd import build_segformer
from src.utils.config import load_config


def load_rgbd_model(
    config_path="deployment/models/rgbd_004_config.yaml",
    checkpoint_path="deployment/models/rgbd_004_best_model.pt",
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = load_config(config_path)

    model = build_segformer(
        model_name=cfg.get("model_name", "nvidia/mit-b0"),
        num_classes=int(cfg["num_classes"]),
        in_channels=4,
        ignore_index=int(cfg.get("ignore_index", 255)),
        pretrained=bool(cfg.get("pretrained", True)),
    )

    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)

    model.to(device)
    model.eval()

    image_size = int(cfg.get("image_size", 512))

    return model, cfg, device, image_size


def preprocess_rgb_frame(rgb_frame, image_size, mean, std):
    if isinstance(rgb_frame, (str, Path)):
        img = Image.open(rgb_frame).convert("RGB").resize((image_size, image_size))
        arr = np.array(img).astype(np.float32) / 255.0

    elif isinstance(rgb_frame, Image.Image):
        img = rgb_frame.convert("RGB").resize((image_size, image_size))
        arr = np.array(img).astype(np.float32) / 255.0

    elif isinstance(rgb_frame, np.ndarray):
        arr = rgb_frame.astype(np.float32)

        if arr.ndim != 3 or arr.shape[2] != 3:
            raise ValueError("RGB frame must have shape H x W x 3.")

        if arr.max() > 1.0:
            arr = arr / 255.0

        img = Image.fromarray((arr * 255).astype(np.uint8)).resize((image_size, image_size))
        arr = np.array(img).astype(np.float32) / 255.0

    else:
        raise TypeError("rgb_frame must be a path, PIL image, or NumPy array.")

    arr = (arr - np.array(mean)) / np.array(std)
    return torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0).float()


def preprocess_depth_frame(depth_frame, image_size):
    if isinstance(depth_frame, (str, Path)):
        depth = np.array(Image.open(depth_frame).resize((image_size, image_size))).astype(np.float32)

    elif isinstance(depth_frame, Image.Image):
        depth = np.array(depth_frame.resize((image_size, image_size))).astype(np.float32)

    elif isinstance(depth_frame, np.ndarray):
        depth = depth_frame.astype(np.float32)

        if depth.ndim == 3:
            depth = depth[:, :, 0]

        depth_img = Image.fromarray(depth.astype(np.float32)).resize((image_size, image_size))
        depth = np.array(depth_img).astype(np.float32)

    else:
        raise TypeError("depth_frame must be a path, PIL image, or NumPy array.")

    valid = depth > 0

    if valid.any():
        p1, p99 = np.percentile(depth[valid], [1, 99])
        depth = np.clip((depth - p1) / (p99 - p1 + 1e-6), 0, 1)
    else:
        depth = np.zeros_like(depth)

    depth = (depth - 0.5) / 0.25

    return torch.from_numpy(depth).unsqueeze(0).unsqueeze(0).float()


def predict_rgbd_mask(model, rgb_frame, depth_frame, cfg, device, image_size):
    rgb_tensor = preprocess_rgb_frame(
        rgb_frame,
        image_size,
        cfg["mean"][:3],
        cfg["std"][:3],
    )

    depth_tensor = preprocess_depth_frame(depth_frame, image_size)

    pixel_values = torch.cat([rgb_tensor, depth_tensor], dim=1).to(device)

    with torch.no_grad():
        outputs = model(pixel_values=pixel_values)
        logits = outputs.logits

        logits = torch.nn.functional.interpolate(
            logits,
            size=(image_size, image_size),
            mode="bilinear",
            align_corners=False,
        )

        pred_mask = torch.argmax(logits, dim=1)[0].cpu().numpy()

    return pred_mask


def decide_navigation(mask):
    h, w = mask.shape

    center = mask[:, w // 3 : 2 * w // 3]
    center_ratio = center.mean()

    if center_ratio > 0.35:
        return "STOP"

    return "MOVE_FORWARD"


def main():
    parser = argparse.ArgumentParser(description="Deploy RGBD_004 SegFormer model.")
    parser.add_argument("--rgb", required=True, help="Path to RGB image.")
    parser.add_argument("--depth", required=True, help="Path to depth image.")
    parser.add_argument("--config", default="deployment/models/rgbd_004_config.yaml")
    parser.add_argument("--checkpoint", default="deployment/models/rgbd_004_best_model.pt")
    args = parser.parse_args()

    model, cfg, device, image_size = load_rgbd_model(args.config, args.checkpoint)

    print(f"Using device: {device}")
    print("RGBD_004 model loaded successfully.")

    # Warm-up
    _ = predict_rgbd_mask(model, args.rgb, args.depth, cfg, device, image_size)

    if device.type == "cuda":
        torch.cuda.synchronize()

    start_time = time.time()

    mask = predict_rgbd_mask(model, args.rgb, args.depth, cfg, device, image_size)

    if device.type == "cuda":
        torch.cuda.synchronize()

    elapsed = time.time() - start_time

    command = decide_navigation(mask)

    print("Prediction complete.")
    print(f"Inference time: {elapsed * 1000:.2f} ms")
    print(f"FPS: {1 / elapsed:.2f}")
    print(f"Navigation command: {command}")


if __name__ == "__main__":
    main()