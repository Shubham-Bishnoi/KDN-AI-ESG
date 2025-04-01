import ee
import geemap
import os
import time

# Initialize Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Load Sentinel-2 dataset
sentinel = ee.ImageCollection("COPERNICUS/S2_SR") \
    .filterDate("2024-01-01", "2024-03-01") \
    .filterBounds(ee.Geometry.Point([78.9629, 20.5937])) \
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10)) \
    .median()

# Compute NDWI (Water Pollution Index)
ndwi = sentinel.normalizedDifference(['B3', 'B8'])  # Green & NIR bands

# Define Different Water Regions for Test Set
test_regions = [
    ee.Geometry.Rectangle([78.5, 20.2, 78.6, 20.3]),
    ee.Geometry.Rectangle([78.7, 20.4, 78.8, 20.5]),
    ee.Geometry.Rectangle([78.9, 20.6, 79.0, 20.7]),
    ee.Geometry.Rectangle([79.1, 20.8, 79.2, 20.9]),
    ee.Geometry.Rectangle([79.3, 21.0, 79.4, 21.1])
]

# Ensure directories exist
test_folder = "data/water_pollution/test"
os.makedirs(test_folder, exist_ok=True)

# Download Sample Test Images
for i, region in enumerate(test_regions):
    filename = f"{test_folder}/ndwi_test_{i}.tif"
    
    try:
        geemap.ee_export_image(ndwi, filename=filename, scale=10, region=region)
        print(f"✅ Test water pollution image {i+1} downloaded!")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        time.sleep(5)

print("✅ All Sample Test Images Downloaded!")
