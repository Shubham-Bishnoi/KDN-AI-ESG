import numpy as np
import rasterio
import tensorflow as tf
import json
import os

# Custom Loss Function (Re-define 'mse' for TensorFlow)
def custom_loss(y_true, y_pred):
    return tf.keras.losses.mean_squared_error(y_true, y_pred)

# Load Trained Models (Recompile)
deforestation_model = tf.keras.models.load_model("models/deforestation_model.h5")
water_pollution_model = tf.keras.models.load_model("models/water_pollution_model.h5")

# Load Biodiversity Model with Custom Loss
biodiversity_model = tf.keras.models.load_model("models/biodiversity_model.h5", compile=False)
biodiversity_model.compile(loss=custom_loss, optimizer="adam")

print(" All models loaded successfully!")

# Define Image Size
IMG_SIZE = (128, 128)

# Function to Load & Preprocess TIFF Images
def load_tiff_image(file_path):
    with rasterio.open(file_path) as dataset:
        image = dataset.read(1)  # Read single-band (grayscale)

        # Apply mean-std normalization instead of min-max scaling
        image = (image - np.mean(image)) / (np.std(image) + 1e-7)

        # Clip values to be between 0 and 1
        image = np.clip(image, 0, 1)

        # Resize image to match model input size
        image_resized = np.resize(image, IMG_SIZE).reshape(1, IMG_SIZE[0], IMG_SIZE[1], 1)

    return image_resized


# Function to Predict Deforestation
def predict_deforestation(image_path):
    image = load_tiff_image(image_path)
    prediction = deforestation_model.predict(image)
    risk_score = prediction[0][0]
    print(f"🌳 Deforestation Risk Score: {risk_score:.4f}")
    return risk_score

# Function to Predict Water Pollution
def predict_water_pollution(image_path):
    image = load_tiff_image(image_path)
    prediction = water_pollution_model.predict(image)
    pollution_score = prediction[0][0]
    print(f"🌊 Water Pollution Score: {pollution_score:.4f}")
    return pollution_score

# Function to Predict Biodiversity Loss
def predict_biodiversity(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    X = []
    for entry in data:
        if "normalized_trend" in entry and len(entry["normalized_trend"]) > 1:
            X.append(entry["normalized_trend"][:-1])  # Features: All years except last

    X = np.array(X).reshape(-1, len(X[0]), 1)  # Reshape for LSTM model
    predictions = biodiversity_model.predict(X)

    avg_loss_risk = np.mean(predictions)
    print(f"🦜 Biodiversity Loss Risk Score: {avg_loss_risk:.4f}")
    return avg_loss_risk

# Example Usage
if __name__ == "__main__":
    deforestation_test_image = "data/deforestation/test/forest_loss_test.tif"
    water_pollution_test_image = "data/water_pollution/test/ndwi_test.tif"
    biodiversity_test_json = "data/biodiversity/test/biodiversity_loss_test.json"

    predict_deforestation(deforestation_test_image)
    predict_water_pollution(water_pollution_test_image)
    predict_biodiversity(biodiversity_test_json)
