from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
DEPTH_EXTENSIONS = IMAGE_EXTENSIONS | {".npy"}


class RGBDGSDDataset(Dataset):
    """
    Dataset for RGB/RGB-D glass surface segmentation.

    Supports either:
      1. Folder-based dataset: split/images, split/masks, split/depth
      2. CSV manifest with columns: rgb, mask, depth
    """

    def __init__(
        self,
        data_root: str | Path,
        split: str,
        modality: str = "rgb",
        image_size: int = 512,
        mean: Optional[List[float]] = None,
        std: Optional[List[float]] = None,
        use_manifest: bool = False,
        manifest_path: Optional[str | Path] = None,
        binary_mask: bool = True,
        ignore_index: int = 255,
        depth_max_value: Optional[float] = None,
    ) -> None:
        self.data_root = Path(data_root)
        self.split = split
        self.modality = modality.lower()
        self.image_size = int(image_size)
        self.binary_mask = bool(binary_mask)
        self.ignore_index = int(ignore_index)
        self.depth_max_value = depth_max_value

        if self.modality not in {"rgb", "rgbd"}:
            raise ValueError("modality must be either 'rgb' or 'rgbd'")

        channels = 4 if self.modality == "rgbd" else 3
        self.mean = np.array(mean if mean is not None else ([0.485, 0.456, 0.406] + ([0.5] if channels == 4 else [])), dtype=np.float32)
        self.std = np.array(std if std is not None else ([0.229, 0.224, 0.225] + ([0.25] if channels == 4 else [])), dtype=np.float32)

        if len(self.mean) != channels or len(self.std) != channels:
            raise ValueError(f"Expected mean/std for {channels} channels, got {len(self.mean)} and {len(self.std)}")

        if use_manifest:
            if manifest_path is None:
                raise ValueError("manifest_path is required when use_manifest=True")
            self.samples = self._load_manifest(manifest_path)
        else:
            self.samples = self._discover_folder_samples()

        if not self.samples:
            raise RuntimeError(f"No samples found for split='{split}' in {self.data_root}")

    def _load_manifest(self, manifest_path: str | Path) -> List[Dict[str, Path]]:
        manifest_path = Path(manifest_path)
        if not manifest_path.is_absolute():
            manifest_path = self.data_root / manifest_path
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        df = pd.read_csv(manifest_path)
        required = {"rgb", "mask"}
        if self.modality == "rgbd":
            required.add("depth")
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Manifest is missing required columns: {sorted(missing)}")

        samples: List[Dict[str, Path]] = []
        for _, row in df.iterrows():
            rgb = self._resolve_path(row["rgb"])
            mask = self._resolve_path(row["mask"])
            depth = self._resolve_path(row["depth"]) if self.modality == "rgbd" and "depth" in row else None
            samples.append({"rgb": rgb, "mask": mask, "depth": depth})
        return samples

    def _discover_folder_samples(self) -> List[Dict[str, Path]]:
        split_dir = self.data_root / self.split
        image_dir = split_dir / "images"
        mask_dir = split_dir / "masks"
        depth_dir = split_dir / "depth"

        if not image_dir.exists():
            raise FileNotFoundError(f"Image folder not found: {image_dir}")
        if not mask_dir.exists():
            raise FileNotFoundError(f"Mask folder not found: {mask_dir}")
        if self.modality == "rgbd" and not depth_dir.exists():
            raise FileNotFoundError(f"Depth folder not found for RGB-D mode: {depth_dir}")

        images = sorted([p for p in image_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS])
        samples: List[Dict[str, Path]] = []
        for rgb_path in images:
            mask_path = self._find_matching_file(mask_dir, rgb_path.stem, IMAGE_EXTENSIONS)
            if mask_path is None:
                continue

            depth_path = None
            if self.modality == "rgbd":
                depth_path = self._find_matching_file(depth_dir, rgb_path.stem, DEPTH_EXTENSIONS)
                if depth_path is None:
                    continue

            samples.append({"rgb": rgb_path, "mask": mask_path, "depth": depth_path})
        return samples

    def _resolve_path(self, path_value: str) -> Path:
        path = Path(str(path_value))
        return path if path.is_absolute() else self.data_root / path

    @staticmethod
    def _find_matching_file(folder: Path, stem: str, extensions: set[str]) -> Optional[Path]:
        for ext in extensions:
            candidate = folder / f"{stem}{ext}"
            if candidate.exists():
                return candidate
        return None

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> Dict[str, torch.Tensor]:
        sample = self.samples[index]

        rgb = self._load_rgb(sample["rgb"])
        mask = self._load_mask(sample["mask"])

        if self.modality == "rgbd":
            if sample["depth"] is None:
                raise RuntimeError("RGB-D sample is missing depth path")
            depth = self._load_depth(sample["depth"])
            image = np.concatenate([rgb, depth[..., None]], axis=-1)
        else:
            image = rgb

        image, mask = self._resize(image, mask)
        image = self._normalise(image)

        image_tensor = torch.from_numpy(image.transpose(2, 0, 1)).float()
        mask_tensor = torch.from_numpy(mask).long()

        return {
            "pixel_values": image_tensor,
            "labels": mask_tensor,
            "rgb_path": str(sample["rgb"]),
            "mask_path": str(sample["mask"]),
        }

    def _load_rgb(self, path: Path) -> np.ndarray:
        if not path.exists():
            raise FileNotFoundError(f"RGB image not found: {path}")
        image = Image.open(path).convert("RGB")
        return np.asarray(image, dtype=np.float32) / 255.0

    def _load_mask(self, path: Path) -> np.ndarray:
        if not path.exists():
            raise FileNotFoundError(f"Mask image not found: {path}")
        mask = Image.open(path)
        mask_np = np.asarray(mask)

        if mask_np.ndim == 3:
            mask_np = mask_np[..., 0]

        mask_np = mask_np.astype(np.int64)
        if self.binary_mask:
            mask_np = (mask_np > 0).astype(np.int64)
        return mask_np

    def _load_depth(self, path: Path) -> np.ndarray:
        if not path.exists():
            raise FileNotFoundError(f"Depth file not found: {path}")

        if path.suffix.lower() == ".npy":
            depth = np.load(path).astype(np.float32)
        else:
            depth = np.asarray(Image.open(path), dtype=np.float32)

        if depth.ndim == 3:
            depth = depth[..., 0]

        valid = np.isfinite(depth)
        depth = np.where(valid, depth, 0.0)

        if self.depth_max_value is not None:
            max_value = float(self.depth_max_value)
            depth = np.clip(depth, 0.0, max_value) / max_value
        else:
            nonzero = depth[depth > 0]
            if nonzero.size > 0:
                low, high = np.percentile(nonzero, [1, 99])
                if high > low:
                    depth = np.clip(depth, low, high)
                    depth = (depth - low) / (high - low)
                else:
                    depth = np.zeros_like(depth, dtype=np.float32)
            else:
                depth = np.zeros_like(depth, dtype=np.float32)

        return depth.astype(np.float32)

    def _resize(self, image: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        size = (self.image_size, self.image_size)
        image_resized = cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)
        mask_resized = cv2.resize(mask.astype(np.int64), size, interpolation=cv2.INTER_NEAREST)
        return image_resized.astype(np.float32), mask_resized.astype(np.int64)

    def _normalise(self, image: np.ndarray) -> np.ndarray:
        return (image - self.mean.reshape(1, 1, -1)) / self.std.reshape(1, 1, -1)
