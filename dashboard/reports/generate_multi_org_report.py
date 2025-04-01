import os  # ✅ Add this line
import json
import pandas as pd
import numpy as np
import tensorflow as tf
import rasterio
import cv2
import ee
import geemap
import time


#  Initialize Google Earth Engine
ee.Initialize(project="ee-sbishnoi29")

#  Load Trained AI Models
deforestation_model = tf.keras.models.load_model("models/deforestation_model.h5")
water_pollution_model = tf.keras.models.load_model("models/water_pollution_model.h5")
biodiversity_model = tf.keras.models.load_model("models/biodiversity_model.h5", compile=False)
biodiversity_model.compile(loss="mse", optimizer="adam")
capital_model = tf.keras.models.load_model("models/natural_capital_model.h5", compile=False)
capital_model.compile(loss="mse", optimizer="adam")

#  Fetch Real-Time Satellite Data
def fetch_real_time_satellite_data(latitude, longitude, save_path):
    try:
        region = ee.Geometry.Point([longitude, latitude]).buffer(2500)

        sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(region) \
            .filterDate("2024-01-01", "2024-12-31") \
            .median()

        ndvi = sentinel.normalizedDifference(['B8', 'B4'])
        ndwi = sentinel.normalizedDifference(['B3', 'B8'])

        os.makedirs(save_path, exist_ok=True)

        geemap.ee_export_image(ndvi, filename=f"{save_path}/ndvi_real_time.tif", scale=10, region=region)
        geemap.ee_export_image(ndwi, filename=f"{save_path}/ndwi_real_time.tif", scale=10, region=region)

        print(f"✅ Real-time satellite data updated at {save_path}")
    except Exception as e:
        print(f" Error fetching real-time satellite data: {e}")

#  Load TIFF Images
def load_tiff(file_path):
    try:
        with rasterio.open(file_path) as dataset:
            image = dataset.read(1)
            image = (image - np.mean(image)) / (np.std(image) + 1e-7)
            image_resized = cv2.resize(image, (128, 128), interpolation=cv2.INTER_AREA)
            return np.clip(image_resized, 0, 1).reshape(1, 128, 128, 1)
    except Exception as e:
        print(f" Error loading TIFF file {file_path}: {e}")
        return np.zeros((1, 128, 128, 1))

#  Generate Real-Time ESG Report
def generate_real_time_esg_report(company_csv, output_json="data/multi_org_report.json"):
    try:
        fetch_real_time_satellite_data(latitude=-3.4653, longitude=-62.2159, save_path="data/geospatial")

        df = pd.read_csv(company_csv)
        df["land_area"] = df["land_area"].astype(float)
        df["biodiversity_index"] = df["biodiversity_index"].astype(float)
        df["carbon_sequestration"] = df["carbon_sequestration"].astype(float)

        reports = {}

        for i, row in df.iterrows():
            print(f" Processing {i+1}/{len(df)}: {row['company']}")

            company_name = row["company"]

            deforestation_risk = deforestation_model.predict(load_tiff("data/geospatial/ndvi_real_time.tif"), verbose=0)[0][0]
            water_pollution = water_pollution_model.predict(load_tiff("data/geospatial/ndwi_real_time.tif"), verbose=0)[0][0]
            biodiversity_loss = np.mean(biodiversity_model.predict(np.array([[row["biodiversity_index"]]]), verbose=0))

            land_type_mapping = {"Forest": 1, "Wetland": 2, "Agricultural": 3, "Urban": 4}
            land_type_numeric = land_type_mapping.get(row["land_type"], 0)

            input_data = np.array([[row["land_area"], land_type_numeric, row["biodiversity_index"], row["carbon_sequestration"]]], dtype=np.float32)
            natural_capital_value = capital_model.predict(input_data, verbose=0)[0][0]

            reports[company_name] = {
                "Deforestation Risk": float(deforestation_risk),
                "Water Pollution Score": float(water_pollution),
                "Biodiversity Loss Risk": float(biodiversity_loss),
                "Natural Capital Value ($)": float(natural_capital_value),
                "Recommendations": [
                    "🌳 Improve forest conservation policies.",
                    "🌊 Reduce industrial water discharge.",
                    "🦜 Increase biodiversity restoration funding."
                ]
            }

        with open(output_json, "w") as f:
            json.dump(reports, f, indent=4)

        print(f" Real-Time Multi-Company ESG Report Updated: {output_json}")

    except Exception as e:
        print(f" Error generating ESG report: {e}")

# Run the Report Generator
generate_real_time_esg_report("data/land_use/organization_land_use.csv")
