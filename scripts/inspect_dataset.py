from PIL import Image
import numpy as np
from pathlib import Path

root = Path("data/RGBD_GSD")

image_path = next((root / "train/images").glob("*"))
mask_path = next((root / "train/masks").glob("*"))
depth_path = next((root / "train/depth").glob("*"))

print("RGB file:", image_path)
print("Mask file:", mask_path)
print("Depth file:", depth_path)

rgb = np.array(Image.open(image_path))
mask = np.array(Image.open(mask_path))
depth = np.array(Image.open(depth_path))

print("\nRGB")
print("Shape:", rgb.shape)
print("Dtype:", rgb.dtype)
print("Min:", rgb.min())
print("Max:", rgb.max())

print("\nMask")
print("Shape:", mask.shape)
print("Dtype:", mask.dtype)
print("Unique values:", np.unique(mask))

print("\nDepth")
print("Shape:", depth.shape)
print("Dtype:", depth.dtype)
print("Min:", depth.min())
print("Max:", depth.max())
print("Unique sample:", np.unique(depth[:20, :20])[:20])