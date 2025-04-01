import os
import cv2
import rasterio
import numpy as np

# Set source and destination folders
input_folder = "data/geospatial/truecolor"
output_folder = "data/geospatial/truecolor/jpg"
os.makedirs(output_folder, exist_ok=True)

# Function to convert .tif to .jpg
def convert_to_jpg(tif_path, jpg_path):
    with rasterio.open(tif_path) as src:
        img = src.read([1, 2, 3])  # Read RGB bands
        img = np.transpose(img, (1, 2, 0))  # Rearrange to (H, W, C)
        img = cv2.convertScaleAbs(img, alpha=(255.0 / 3000.0))  # Normalize to 0–255
        cv2.imwrite(jpg_path, img)
        print(f" JPG saved at: {jpg_path}")

# Convert all .tif files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        tif_path = os.path.join(input_folder, filename)
        jpg_name = filename.replace(".tif", ".jpg")
        jpg_path = os.path.join(output_folder, jpg_name)
        convert_to_jpg(tif_path, jpg_path)

print("🎉 All TIF images converted to JPG successfully!")
