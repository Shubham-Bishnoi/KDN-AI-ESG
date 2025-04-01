import ee
import geemap
import time
import os

# Initialize Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Ensure directories exist
train_folder = "data/geospatial/train"
test_folder = "data/geospatial/test"
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Define **multiple** locations for **better variety**
locations = [
    (-3.4653, -62.2159, "Amazon Rainforest"),  # Dense Forest
    (37.7749, -122.4194, "San Francisco Bay"),  # Coastal Water
    (51.5074, -0.1278, "London River Thames"),  # Urban River
    (20.5937, 78.9629, "India Ganges River"),  # Ganges River
    (34.0522, -118.2437, "Los Angeles Urban"),  # Urban Area
]

# Function to fetch **real-time NDVI & NDWI** satellite data
def get_real_time_satellite_data(latitude, longitude, start_date, end_date, save_path, file_prefix):
    try:
        region = ee.Geometry.Point([longitude, latitude]).buffer(5000)  # 5km buffer for better details

        # Load Sentinel-2 Harmonized Dataset
        sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .median()

        # Compute NDVI & NDWI
        ndvi = sentinel.normalizedDifference(['B8', 'B4'])  # Vegetation Index
        ndwi = sentinel.normalizedDifference(['B3', 'B8'])  # Water Quality Index

        # Ensure Save Directory Exists
        os.makedirs(save_path, exist_ok=True)

        # Retry Mechanism
        for attempt in range(3):
            try:
                print(f" Attempt {attempt + 1}: Fetching NDVI & NDWI for {file_prefix}...")

                # Save as GeoTIFF
                geemap.ee_export_image(ndvi, filename=f"{save_path}/{file_prefix}_ndvi.tif", scale=10, region=region)
                geemap.ee_export_image(ndwi, filename=f"{save_path}/{file_prefix}_ndwi.tif", scale=10, region=region)
                
                print(f"{file_prefix} satellite data saved at {save_path}")
                break  # Exit retry loop if successful
            except Exception as e:
                print(f" Error downloading {file_prefix} data (Attempt {attempt + 1}): {e}")
                time.sleep(5)  # Wait before retrying

    except Exception as main_error:
        print(f" Failed to fetch real-time satellite data: {main_error}")

# Download 5 Train + 5 Test images
for idx, (lat, lon, name) in enumerate(locations):
    file_prefix_train = f"train_{idx}_{name.replace(' ', '_')}"
    file_prefix_test = f"test_{idx}_{name.replace(' ', '_')}"

    # Alternate between train and test datasets
    get_real_time_satellite_data(lat, lon, "2023-01-01", "2023-12-31", train_folder, file_prefix_train)
    get_real_time_satellite_data(lat, lon, "2023-01-01", "2023-12-31", test_folder, file_prefix_test)

print(" All real-time satellite images downloaded successfully!")
