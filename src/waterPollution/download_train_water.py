import ee
import geemap
import os
import time
import random

#  Initialize Google Earth Engine
ee.Initialize(project="ee-sbishnoi29")

# Load Sentinel-2 Surface Reflectance Collection
sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterDate("2024-01-01", "2024-03-01") \
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10)) \
    .mosaic()

#  Compute NDWI (Water Index)
ndwi = sentinel.normalizedDifference(["B3", "B8"]).rename("NDWI")

#  Rescale NDWI from -1 to 1 → 0 to 255
ndwi_rescaled = ndwi.multiply(127.5).add(127.5).clamp(0, 255).byte()

#  Apply Color Palette (Brown = Land, White = Transition, Blue = Water)
ndwi_colored = ndwi_rescaled.visualize(min=0, max=255, palette=["brown", "white", "blue"])

#  Define Water-Rich Regions with Larger Coverage
regions = {
    "Great_Lakes_NA": ee.Geometry.Rectangle([-90.0, 42.0, -80.0, 48.0]),
    "Amazon_Basin_Brazil": ee.Geometry.Rectangle([-70.0, -10.0, -55.0, 0.0]),
    "Lake_Baikal_Russia": ee.Geometry.Rectangle([105.0, 52.0, 110.0, 56.0]),
    "Kerala_Backwaters_India": ee.Geometry.Rectangle([75.8, 8.5, 77.2, 10.5]),
    "Congo_River_Africa": ee.Geometry.Rectangle([14.0, -5.0, 18.0, 1.0]),
    "Mekong_Delta_Vietnam": ee.Geometry.Rectangle([104.5, 9.0, 106.5, 11.0]),
    "Mississippi_Delta_USA": ee.Geometry.Rectangle([-91.0, 28.0, -88.0, 31.0]),
    "Lake_Victoria_Africa": ee.Geometry.Rectangle([31.0, -3.0, 35.0, 2.0]),
    "Caspian_Sea_Eurasia": ee.Geometry.Rectangle([47.0, 38.0, 54.0, 46.0]),
    "Scandinavian_Lakes_Europe": ee.Geometry.Rectangle([24.0, 59.0, 30.0, 63.0]),
}

#  Ensure Output Directory Exists
output_folder = "data/water_pollution/train"
os.makedirs(output_folder, exist_ok=True)

#  Generate 1000 Images (100 per Region × 10 Regions)
exported_files = []
for region_name, bbox in regions.items():
    for i in range(100):  # Generate 100 images per region
        # Randomly select a smaller section from the large region
        min_lon, min_lat, max_lon, max_lat = bbox.getInfo()['coordinates'][0][0][0], bbox.getInfo()['coordinates'][0][0][1], \
                                             bbox.getInfo()['coordinates'][0][2][0], bbox.getInfo()['coordinates'][0][2][1]
        random_lon = random.uniform(min_lon, max_lon)
        random_lat = random.uniform(min_lat, max_lat)

        # Create a small 5km x 5km box instead of a single point
        small_region = ee.Geometry.Rectangle([
            [random_lon - 0.025, random_lat - 0.025],
            [random_lon + 0.025, random_lat + 0.025]
        ])

        filename = f"{output_folder}/{region_name}_image_{i}.tif"
        try:
            geemap.ee_export_image(
                ndwi_colored,
                filename=filename,
                scale=10,  # Higher resolution (10m)
                region=small_region  # Smaller but more detailed images
            )
            exported_files.append(filename)
            print(f" NDWI Image {i+1} for {region_name} downloaded!")
        except Exception as e:
            print(f" Error downloading {region_name} image {i+1}: {e}")
            time.sleep(5)

print(" All NDWI Images Successfully Downloaded!")
