from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from src.train import build_loader, evaluate
from src.models.segformer_rgbd import build_segformer
from src.utils.config import load_config
from src.utils.seed import set_seed


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained SegFormer RGB/RGB-D model")
    parser.add_argument("--checkpoint", required=True, help="Path to checkpoint .pt file")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--split", default="test", choices=["train", "val", "test"], help="Dataset split to evaluate")
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(int(cfg.get("seed", 42)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    in_channels = 4 if cfg["modality"].lower() == "rgbd" else 3

    loader = build_loader(cfg, args.split, shuffle=False)
    model = build_segformer(
        model_name=cfg.get("model_name", "nvidia/mit-b0"),
        num_classes=int(cfg["num_classes"]),
        in_channels=in_channels,
        ignore_index=int(cfg.get("ignore_index", 255)),
        pretrained=bool(cfg.get("pretrained", True)),
    ).to(device)

    checkpoint = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)

    result = evaluate(model, loader, device, cfg)
    print(json.dumps(result, indent=2))

    output_dir = Path(cfg.get("output_dir", "outputs/experiment"))
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{args.split}_metrics.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved metrics to: {out_path}")


if __name__ == "__main__":
    main()
