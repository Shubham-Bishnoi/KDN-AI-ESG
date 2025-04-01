import ee
import geemap
import os
import zipfile
import time

# Initialize Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Load Global Forest Change Dataset (Deforestation Data)
forest_loss = ee.Image("UMD/hansen/global_forest_change_2022_v1_10").select('loss')

# Define latitude & longitude range (Different from Train)
latitudes = list(range(-25, -5))  # Different range to increase variety
longitudes = list(range(-90, -70))  # Different region for diversity

# Ensure test directory exists
test_folder = "data/deforestation/test"
os.makedirs(test_folder, exist_ok=True)

# Download 1000 Test Images
test_count = 0
max_test = 1000
max_attempts = 5  # Retry up to 5 times for each image

for lat in latitudes:
    for lon in longitudes:
        if test_count >= max_test:
            break  # Stop when we have 1000 images

        # Define a 1°x1° tile region
        region = ee.Geometry.Rectangle([lon, lat, lon + 1, lat + 1])

        filename = f"{test_folder}/forest_loss_test_{test_count}.tif"
        test_count += 1

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

print(" 1000 Testing Deforestation Images Downloaded Successfully!")

# Zip the test images
zip_path = "data/deforestation/deforestation_test.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(test_folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), test_folder))
print(f"= {zip_path} created!")
