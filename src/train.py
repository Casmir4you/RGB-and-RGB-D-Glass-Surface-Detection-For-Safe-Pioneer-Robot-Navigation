from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict

import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.datasets.rgbd_gsd_dataset import RGBDGSDDataset
from src.models.segformer_rgbd import build_segformer
from src.utils.config import ensure_output_dir, load_config
from src.utils.metrics import SegmentationMetrics
from src.utils.seed import set_seed


def build_dataset(cfg: Dict, split: str) -> RGBDGSDDataset:
    manifest_key = f"{split}_manifest"
    return RGBDGSDDataset(
        data_root=cfg["data_root"],
        split=cfg.get(f"{split}_split", split),
        modality=cfg["modality"],
        image_size=cfg["image_size"],
        mean=cfg["mean"],
        std=cfg["std"],
        use_manifest=cfg.get("use_manifest", False),
        manifest_path=cfg.get(manifest_key),
        binary_mask=cfg.get("binary_mask", True),
        ignore_index=cfg.get("ignore_index", 255),
        depth_max_value=cfg.get("depth_max_value"),
    )


def build_loader(cfg: Dict, split: str, shuffle: bool) -> DataLoader:
    dataset = build_dataset(cfg, split)
    return DataLoader(
        dataset,
        batch_size=int(cfg["batch_size"]),
        shuffle=shuffle,
        num_workers=int(cfg.get("num_workers", 4)),
        pin_memory=torch.cuda.is_available(),
        drop_last=split == "train",
    )


def train_one_epoch(model, loader, optimizer, scaler, device, cfg) -> float:
    model.train()
    total_loss = 0.0
    num_batches = 0
    use_amp = bool(cfg.get("mixed_precision", True)) and device.type == "cuda"

    for batch in tqdm(loader, desc="Training", leave=False):
        pixel_values = batch["pixel_values"].to(device, non_blocking=True)
        labels = batch["labels"].to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        with torch.cuda.amp.autocast(enabled=use_amp):
            outputs = model(pixel_values=pixel_values, labels=labels)
            loss = outputs.loss

        scaler.scale(loss).backward()

        grad_clip = cfg.get("grad_clip_norm")
        if grad_clip is not None:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), float(grad_clip))

        scaler.step(optimizer)
        scaler.update()

        total_loss += float(loss.item())
        num_batches += 1

    return total_loss / max(num_batches, 1)


@torch.no_grad()
def evaluate(model, loader, device, cfg) -> Dict[str, float]:
    model.eval()
    metrics = SegmentationMetrics(
        num_classes=int(cfg["num_classes"]),
        ignore_index=int(cfg.get("ignore_index", 255)),
        glass_class_id=int(cfg.get("glass_class_id", 1)),
    )

    total_loss = 0.0
    num_batches = 0
    total_time = 0.0
    total_images = 0

    for batch in tqdm(loader, desc="Validation", leave=False):
        pixel_values = batch["pixel_values"].to(device, non_blocking=True)
        labels = batch["labels"].to(device, non_blocking=True)

        if device.type == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()

        outputs = model(pixel_values=pixel_values, labels=labels)
        logits = outputs.logits

        logits_up = F.interpolate(
            logits,
            size=labels.shape[-2:],
            mode="bilinear",
            align_corners=False,
        )
        preds = torch.argmax(logits_up, dim=1)

        if device.type == "cuda":
            torch.cuda.synchronize()
        elapsed = time.perf_counter() - start

        metrics.update(preds, labels)
        total_loss += float(outputs.loss.item())
        num_batches += 1
        total_time += elapsed
        total_images += pixel_values.shape[0]

    result = metrics.compute()
    result["loss"] = total_loss / max(num_batches, 1)
    result["inference_time_ms"] = 1000.0 * total_time / max(total_images, 1)
    result["fps"] = total_images / total_time if total_time > 0 else 0.0
    return result


def save_checkpoint(path: Path, model, optimizer, scheduler, epoch: int, best_metric: float, cfg: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict() if scheduler is not None else None,
            "best_metric": best_metric,
            "config": cfg,
        },
        path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train SegFormer RGB/RGB-D glass segmentation model")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(int(cfg.get("seed", 42)))
    output_dir = ensure_output_dir(cfg)

    with (output_dir / "config_used.json").open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    in_channels = 4 if cfg["modality"].lower() == "rgbd" else 3

    train_loader = build_loader(cfg, "train", shuffle=True)
    val_loader = build_loader(cfg, "val", shuffle=False)

    model = build_segformer(
        model_name=cfg.get("model_name", "nvidia/mit-b0"),
        num_classes=int(cfg["num_classes"]),
        in_channels=in_channels,
        ignore_index=int(cfg.get("ignore_index", 255)),
        pretrained=bool(cfg.get("pretrained", True)),
    ).to(device)

    optimizer = AdamW(
        model.parameters(),
        lr=float(cfg["learning_rate"]),
        weight_decay=float(cfg.get("weight_decay", 0.01)),
    )

    epochs = int(cfg["epochs"])
    warmup_epochs = int(cfg.get("warmup_epochs", 0))
    if warmup_epochs > 0:
        warmup = LinearLR(optimizer, start_factor=0.1, total_iters=warmup_epochs)
        cosine = CosineAnnealingLR(optimizer, T_max=max(epochs - warmup_epochs, 1))
        scheduler = SequentialLR(optimizer, schedulers=[warmup, cosine], milestones=[warmup_epochs])
    else:
        scheduler = CosineAnnealingLR(optimizer, T_max=epochs)

    scaler = torch.cuda.amp.GradScaler(enabled=bool(cfg.get("mixed_precision", True)) and device.type == "cuda")

    best_metric_name = cfg.get("save_best_metric", "mean_iou")
    best_metric = -1.0
    patience = int(cfg.get("early_stopping_patience", 12))
    epochs_without_improvement = 0
    history = []

    print(f"Using device: {device}")
    print(f"Training modality: {cfg['modality']}")
    print(f"Train samples: {len(train_loader.dataset)} | Val samples: {len(val_loader.dataset)}")

    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(model, train_loader, optimizer, scaler, device, cfg)
        val_result = evaluate(model, val_loader, device, cfg)
        scheduler.step()

        current_metric = float(val_result.get(best_metric_name, 0.0))
        improved = current_metric > best_metric
        if improved:
            best_metric = current_metric
            epochs_without_improvement = 0
            save_checkpoint(output_dir / "best_model.pt", model, optimizer, scheduler, epoch, best_metric, cfg)
        else:
            epochs_without_improvement += 1

        epoch_record = {
            "epoch": epoch,
            "train_loss": train_loss,
            **val_result,
            "best_metric": best_metric,
            "learning_rate": optimizer.param_groups[0]["lr"],
        }
        history.append(epoch_record)

        with (output_dir / "history.json").open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        print(
            f"Epoch {epoch:03d}/{epochs} | "
            f"train_loss={train_loss:.4f} | "
            f"val_loss={val_result['loss']:.4f} | "
            f"mIoU={val_result['mean_iou']:.4f} | "
            f"glass_IoU={val_result['glass_iou']:.4f} | "
            f"glass_F1={val_result['glass_f1']:.4f} | "
            f"FPS={val_result['fps']:.2f}"
        )

        save_checkpoint(output_dir / "last_model.pt", model, optimizer, scheduler, epoch, best_metric, cfg)

        if epochs_without_improvement >= patience:
            print(f"Early stopping after {patience} epochs without improvement.")
            break

    print(f"Training complete. Best {best_metric_name}: {best_metric:.4f}")
    print(f"Best checkpoint: {output_dir / 'best_model.pt'}")


if __name__ == "__main__":
    main()
