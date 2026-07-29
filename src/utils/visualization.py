from __future__ import annotations

from pathlib import Path
import cv2
import numpy as np
from PIL import Image


def save_mask_overlay(
    rgb_path: str | Path,
    pred_mask: np.ndarray,
    output_path: str | Path,
    alpha: float = 0.45,
    glass_class_id: int = 1,
) -> None:
    """Save a visual overlay of the predicted glass mask on the RGB image."""
    rgb = np.array(Image.open(rgb_path).convert("RGB"))
    pred_mask = pred_mask.astype(np.uint8)

    if pred_mask.shape[:2] != rgb.shape[:2]:
        pred_mask = cv2.resize(pred_mask, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_NEAREST)

    overlay = rgb.copy()
    glass = pred_mask == glass_class_id
    overlay[glass] = [255, 0, 0]

    blended = (alpha * overlay + (1.0 - alpha) * rgb).astype(np.uint8)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(blended).save(output_path)
