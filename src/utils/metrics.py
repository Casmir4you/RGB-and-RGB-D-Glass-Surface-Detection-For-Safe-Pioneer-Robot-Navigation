from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import numpy as np
import torch


@dataclass
class SegmentationMetrics:
    num_classes: int
    ignore_index: int = 255
    glass_class_id: int = 1

    def __post_init__(self) -> None:
        self.confusion = np.zeros((self.num_classes, self.num_classes), dtype=np.int64)

    def reset(self) -> None:
        self.confusion.fill(0)

    @torch.no_grad()
    def update(self, preds: torch.Tensor, targets: torch.Tensor) -> None:
        """
        Update confusion matrix.

        Args:
            preds: Tensor [B, H, W] containing class IDs.
            targets: Tensor [B, H, W] containing class IDs.
        """
        preds_np = preds.detach().cpu().numpy().astype(np.int64)
        targets_np = targets.detach().cpu().numpy().astype(np.int64)

        valid = targets_np != self.ignore_index
        valid &= targets_np >= 0
        valid &= targets_np < self.num_classes

        labels = self.num_classes * targets_np[valid] + preds_np[valid]
        counts = np.bincount(labels, minlength=self.num_classes ** 2)
        self.confusion += counts.reshape(self.num_classes, self.num_classes)

    def compute(self) -> Dict[str, float]:
        hist = self.confusion.astype(np.float64)
        tp = np.diag(hist)
        fp = hist.sum(axis=0) - tp
        fn = hist.sum(axis=1) - tp
        total = hist.sum()

        union = tp + fp + fn
        iou = np.divide(tp, union, out=np.zeros_like(tp), where=union > 0)
        precision = np.divide(tp, tp + fp, out=np.zeros_like(tp), where=(tp + fp) > 0)
        recall = np.divide(tp, tp + fn, out=np.zeros_like(tp), where=(tp + fn) > 0)
        f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros_like(tp), where=(precision + recall) > 0)

        pixel_accuracy = float(tp.sum() / total) if total > 0 else 0.0
        mean_iou = float(np.nanmean(iou))

        g = int(self.glass_class_id)
        result = {
            "pixel_accuracy": pixel_accuracy,
            "mean_iou": mean_iou,
            "glass_iou": float(iou[g]) if g < self.num_classes else 0.0,
            "glass_precision": float(precision[g]) if g < self.num_classes else 0.0,
            "glass_recall": float(recall[g]) if g < self.num_classes else 0.0,
            "glass_f1": float(f1[g]) if g < self.num_classes else 0.0,
        }

        for class_id in range(self.num_classes):
            result[f"class_{class_id}_iou"] = float(iou[class_id])
            result[f"class_{class_id}_precision"] = float(precision[class_id])
            result[f"class_{class_id}_recall"] = float(recall[class_id])
            result[f"class_{class_id}_f1"] = float(f1[class_id])

        return result
