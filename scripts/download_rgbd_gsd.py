from datasets import load_dataset

dataset_name = "garrying/RGBD-GSD"

print("Downloading dataset...")
ds = load_dataset(dataset_name)

print(ds)

for split_name, split_data in ds.items():
    print(f"\nSplit: {split_name}")
    print(split_data)
    print("Columns:", split_data.column_names)
    print("First sample:", split_data[0])