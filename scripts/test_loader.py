import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from src.datasets.rgbd_gsd_dataset import RGBDGSDDataset

root = "data/RGBD_GSD"

rgb_ds = RGBDGSDDataset(
    data_root=root,
    split="train",
    modality="rgb",
    image_size=512,
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225],
    use_manifest=True,
    manifest_path="train.csv",
    ignore_index=255,
    binary_mask=True,
)

rgbd_ds = RGBDGSDDataset(
    data_root=root,
    split="train",
    modality="rgbd",
    image_size=512,
    mean=[0.485, 0.456, 0.406, 0.5],
    std=[0.229, 0.224, 0.225, 0.25],
    use_manifest=True,
    manifest_path="train.csv",
    ignore_index=255,
    binary_mask=True,
)

print("RGB dataset length:", len(rgb_ds))
sample_rgb = rgb_ds[0]
print("RGB pixel_values shape:", sample_rgb["pixel_values"].shape)
print("RGB label shape:", sample_rgb["labels"].shape)
print("RGB label unique:", sample_rgb["labels"].unique())

print("\nRGB-D dataset length:", len(rgbd_ds))
sample_rgbd = rgbd_ds[0]
print("RGB-D pixel_values shape:", sample_rgbd["pixel_values"].shape)
print("RGB-D label shape:", sample_rgbd["labels"].shape)
print("RGB-D label unique:", sample_rgbd["labels"].unique())