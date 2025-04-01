import os
import rasterio
import numpy as np
import cv2

# Define input & output directories for deforestation
dataset = {
    "train": "data/deforestation/train",
    "test": "data/deforestation/test",
    "output": "data/deforestation/visualized"
}

# Ensure output folders exist
os.makedirs(dataset["output"], exist_ok=True)

# Function to convert .tif to .jpg with brightness adjustment
def convert_tif_to_jpg(tif_path, jpg_path):
    with rasterio.open(tif_path) as dataset:
        image = dataset.read(1)  # Read single-band NDVI

        # **Fix: Normalize between 0-255**
        image = (image - image.min()) / (image.max() - image.min() + 1e-7) * 255
        image = image.astype(np.uint8)  # Convert to 8-bit grayscale

        # **Apply CLAHE (Adaptive Histogram Equalization)**
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        image = clahe.apply(image)

        # Save as JPG
        cv2.imwrite(jpg_path, image)
        print(f"✅ Converted: {jpg_path}")

# Process images for deforestation dataset (train & test)
for data_type in ["train", "test"]:
    input_folder = dataset[data_type]
    output_folder = dataset["output"]

    for filename in os.listdir(input_folder):
        if filename.endswith(".tif"):
            tif_path = os.path.join(input_folder, filename)
            jpg_path = os.path.join(output_folder, filename.replace(".tif", ".jpg"))
            convert_tif_to_jpg(tif_path, jpg_path)

print("🎉 All deforestation images converted successfully!")
