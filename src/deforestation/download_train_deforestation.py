import ee
import geemap
import os
import zipfile
import time

# Initialize Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Load Global Forest Change Dataset (Deforestation Data)
forest_loss = ee.Image("UMD/hansen/global_forest_change_2022_v1_10").select('loss')

# Define latitude & longitude range (Amazon Rainforest)
latitudes = list(range(-15, 15))  # Expanded range from -15° to +15°
longitudes = list(range(-85, -55))  # Expanded range from -85° to -55°

# Ensure train directory exists
train_folder = "data/deforestation/train"
os.makedirs(train_folder, exist_ok=True)

# Download 1000 Train Images
train_count = 0
max_train = 1000
max_attempts = 5  # Retry up to 5 times for each image

for lat in latitudes:
    for lon in longitudes:
        if train_count >= max_train:
            break  # Stop when we have 10000 images

        # Define a 1°x1° tile region
        region = ee.Geometry.Rectangle([lon, lat, lon + 1, lat + 1])

        filename = f"{train_folder}/forest_loss_train_{train_count}.tif"
        train_count += 1

        # Download with retries
        success = False
        for attempt in range(max_attempts):
            try:
                geemap.ee_export_image(forest_loss, filename=filename, scale=30, region=region)
                print(f" Image saved: {filename}")
                success = True
                break  # Exit retry loop if successful
            except Exception as e:
                print(f" Error downloading {filename} (Attempt {attempt+1}/{max_attempts}): {e}")
                time.sleep(5)  # Wait before retrying

        if not success:
            print(f" Skipping {filename} after {max_attempts} failed attempts.")

print(" 10000 Training Deforestation Images Downloaded Successfully!")

# Zip the train images
zip_path = "data/deforestation/deforestation_train.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(train_folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), train_folder))
print(f" {zip_path} created!")
