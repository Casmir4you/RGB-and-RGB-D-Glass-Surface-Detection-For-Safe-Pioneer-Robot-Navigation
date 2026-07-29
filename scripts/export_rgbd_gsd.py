from datasets import load_dataset
from pathlib import Path
import random
import csv

SEED = 42
DATASET_NAME = "garrying/RGBD-GSD"

root = Path("data/RGBD_GSD")
splits = {
    "train": root / "train",
    "val": root / "val",
    "test": root / "test",
}

for split_dir in splits.values():
    (split_dir / "images").mkdir(parents=True, exist_ok=True)
    (split_dir / "masks").mkdir(parents=True, exist_ok=True)
    (split_dir / "depth").mkdir(parents=True, exist_ok=True)

print("Loading dataset from Hugging Face cache...")
ds = load_dataset(DATASET_NAME)

train_data = list(ds["train"])
test_data = list(ds["test"])

random.seed(SEED)
random.shuffle(train_data)

our_train = train_data[:2040]
our_val = train_data[2040:2400]
our_test = test_data

print(f"Train: {len(our_train)}")
print(f"Val: {len(our_val)}")
print(f"Test: {len(our_test)}")

def save_split(samples, split_name):
    manifest_rows = []
    split_dir = splits[split_name]

    for item in samples:
        image_id = str(item["image_id"])

        rgb_path = split_dir / "images" / f"{image_id}.jpg"
        mask_path = split_dir / "masks" / f"{image_id}.png"
        depth_path = split_dir / "depth" / f"{image_id}.png"

        item["image"].save(rgb_path)
        item["mask"].save(mask_path)
        item["depth"].save(depth_path)

        manifest_rows.append({
            "rgb": str(rgb_path.relative_to(root)),
            "mask": str(mask_path.relative_to(root)),
            "depth": str(depth_path.relative_to(root)),
        })

    manifest_path = root / f"{split_name}.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rgb", "mask", "depth"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    print(f"Saved {split_name}: {len(samples)} samples")
    print(f"Manifest: {manifest_path}")

save_split(our_train, "train")
save_split(our_val, "val")
save_split(our_test, "test")

print("Export complete.")