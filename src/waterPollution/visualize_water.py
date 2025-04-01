import os
import rasterio
import numpy as np
import cv2

# ✅ Define Input & Output Folders
train_folder = "data/water_pollution/train"
output_folder = "data/water_pollution/visualized"
os.makedirs(output_folder, exist_ok=True)

# ✅ Function to Convert .TIF to Colorized .JPG
def convert_tif_to_jpg(tif_path, jpg_path):
    with rasterio.open(tif_path) as dataset:
        image = dataset.read(1)  # Read Single-Band NDWI

        # ✅ Proper Min-Max Scaling
        image = ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(np.uint8)

        # ✅ Apply Jet Colormap (Better Contrast for NDWI)
        image_colored = cv2.applyColorMap(image, cv2.COLORMAP_JET)

        # ✅ Save Image as JPG
        cv2.imwrite(jpg_path, image_colored)
        print(f"✅ Converted: {jpg_path}")

# ✅ Process All Exported Images
for filename in os.listdir(train_folder):
    if filename.endswith(".tif"):
        tif_path = os.path.join(train_folder, filename)
        jpg_path = os.path.join(output_folder, filename.replace(".tif", ".jpg"))
        convert_tif_to_jpg(tif_path, jpg_path)

print("✅ All Water Pollution Images Converted Successfully!")
