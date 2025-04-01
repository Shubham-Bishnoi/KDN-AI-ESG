import json
import numpy as np
import rasterio
import tensorflow as tf

# Load Trained Models
deforestation_model = tf.keras.models.load_model("models/deforestation_model.h5")
water_pollution_model = tf.keras.models.load_model("models/water_pollution_model.h5")
biodiversity_model = tf.keras.models.load_model("models/biodiversity_model.h5", compile=False)
biodiversity_model.compile(loss="mse", optimizer="adam")  # Recompile if needed

# Define Image Size
IMG_SIZE = (128, 128)

# Function to Load & Preprocess TIFF Images
def load_tiff_image(file_path):
    with rasterio.open(file_path) as dataset:
        image = dataset.read(1)  # Read single-band (grayscale)
        image = (image - np.mean(image)) / (np.std(image) + 1e-7)  # Standardize
        image = np.clip(image, 0, 1)
        image_resized = np.resize(image, IMG_SIZE).reshape(1, IMG_SIZE[0], IMG_SIZE[1], 1)
    return image_resized

# Function to Predict Deforestation
def predict_deforestation(image_path):
    image = load_tiff_image(image_path)
    prediction = deforestation_model.predict(image)
    return float(prediction[0][0])

# Function to Predict Water Pollution
def predict_water_pollution(image_path):
    image = load_tiff_image(image_path)
    prediction = water_pollution_model.predict(image)
    return float(prediction[0][0])

# Function to Predict Biodiversity Loss
def predict_biodiversity(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    X = []
    for entry in data:
        if "normalized_trend" in entry and len(entry["normalized_trend"]) > 1:
            X.append(entry["normalized_trend"][:-1])
    X = np.array(X).reshape(-1, len(X[0]), 1)
    predictions = biodiversity_model.predict(X)
    return float(np.mean(predictions))

# Generate ESG Report
def generate_esg_report(deforestation_image, water_image, biodiversity_json, output_file="data/esg_report.json"):
    report = {
        "Deforestation Risk Score": predict_deforestation(deforestation_image),
        "Water Pollution Score": predict_water_pollution(water_image),
        "Biodiversity Loss Risk Score": predict_biodiversity(biodiversity_json),
        "Recommendations": [
            "🌳 Implement reforestation projects in high-risk deforestation zones.",
            "🌊 Strengthen wetland protection policies to reduce water pollution.",
            "🦜 Establish wildlife corridors to maintain biodiversity balance."
        ],
        "TNFD Compliance": {
            "Framework": "Task Force on Nature-Related Financial Disclosures (TNFD)",
            "Scope": "Environmental Risk & Natural Capital Valuation",
            "Impact Areas": ["Forests", "Water Bodies", "Biodiversity"]
        }
    }

    # Save Report
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)
    
    print(f" ESG Biodiversity Impact Report Generated: {output_file}")

# Example Usage
if __name__ == "__main__":
    deforestation_test_image = "data/deforestation/test/forest_loss_test.tif"
    water_pollution_test_image = "data/water_pollution/test/ndwi_test.tif"
    biodiversity_test_json = "data/biodiversity/test/biodiversity_loss_test.json"

    generate_esg_report(deforestation_test_image, water_pollution_test_image, biodiversity_test_json)
