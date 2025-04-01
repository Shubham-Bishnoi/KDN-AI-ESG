import ee
import geemap
import os
import time

# Initialize Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Output directory
output_dir = "data/geospatial/truecolor"
os.makedirs(output_dir, exist_ok=True)

# Locations to download
locations = {
    "Amazon_Rainforest": [-62.2159, -3.4653],
    "Great_Wall_of_China": [116.5704, 40.4319],
    "Pyramids_of_Giza": [31.1342, 29.9792],
    "Eiffel_Tower": [2.2945, 48.8584],
    "Sydney_Opera_House": [151.2153, -33.8572],
    "Grand_Canyon": [-112.1130, 36.1069],
    "Mount_Everest": [86.9250, 27.9881],
    "Sahara_Desert": [13.1711, 23.4162],
    "Antarctica": [11.8650, -75.2500],
}

# Download each location
for name, (lon, lat) in locations.items():
    try:
        region = ee.Geometry.Point([lon, lat]).buffer(2500).bounds()

        # Get Sentinel-2 surface reflectance, filter for cloud-free
        image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(region) \
            .filterDate("2023-01-01", "2023-12-31") \
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10)) \
            .median() \
            .select(['B4', 'B3', 'B2'])  # RGB bands

        # Set visualization
        vis_params = {
            'min': 0,
            'max': 3000,
            'bands': ['B4', 'B3', 'B2']
        }

        # Output file path
        tif_path = os.path.join(output_dir, f"{name}.tif")

        # Export image
        print(f"Exporting {name}...")
        geemap.ee_export_image(
            image.visualize(**vis_params),
            filename=tif_path,
            scale=10,
            region=region
        )
        print(f" Exported: {tif_path}")

    except Exception as e:
        print(f" Error exporting {name}: {e}")
        time.sleep(3)

print(" All true color images exported successfully.")
