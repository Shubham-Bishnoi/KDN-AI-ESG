import os
import rasterio
import numpy as np
import cv2
import argparse

# Define dataset paths
DATASETS = {
    "deforestation": {
        "train": "data/deforestation/train",
        "test": "data/deforestation/test",
        "output": "data/deforestation/processed"
    },
    "water_pollution": {
        "train": "data/water_pollution/train",
        "test": "data/water_pollution/test",
        "output": "data/water_pollution/processed"
    },
    "biodiversity": {
        "train": "data/biodiversity/train",
        "test": "data/biodiversity/test",
        "output": "data/biodiversity/processed"
    }
}

# Ensure output folders exist
for dataset in DATASETS.values():
    os.makedirs(dataset["output"], exist_ok=True)

# Function to preprocess .tif images and save them as .jpg
def preprocess_image(tif_path, jpg_path):
    with rasterio.open(tif_path) as dataset:
        image = dataset.read(1)  # Read single-band grayscale

        # Normalize image (0-255 scaling)
        image = (image - image.min()) / (image.max() - image.min() + 1e-7) * 255
        image = image.astype(np.uint8)  # Convert to 8-bit

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        image = clahe.apply(image)

        # Save processed image
        cv2.imwrite(jpg_path, image)
        print(f" Processed: {jpg_path}")

# Main function to process images for a given dataset
def process_dataset(dataset_name):
    if dataset_name not in DATASETS:
        print(f"Error: Dataset '{dataset_name}' not found. Choose from: {list(DATASETS.keys())}")
        return

    paths = DATASETS[dataset_name]

    for data_type in ["train", "test"]:
        input_folder = paths[data_type]
        output_folder = paths["output"]

        for filename in os.listdir(input_folder):
            if filename.endswith(".tif"):
                tif_path = os.path.join(input_folder, filename)
                jpg_path = os.path.join(output_folder, filename.replace(".tif", ".jpg"))
                preprocess_image(tif_path, jpg_path)

    print(f" All {dataset_name} images processed successfully!")

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess satellite images for AI training.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset to process: deforestation, water_pollution, biodiversity")
    
    args = parser.parse_args()
    process_dataset(args.dataset)
