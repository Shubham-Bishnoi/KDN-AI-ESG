import numpy as np
import json
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load Biodiversity Data from JSON
def load_biodiversity_data(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    # Extract normalized population trends
    X, y = [], []
    for entry in data:
        if "normalized_trend" in entry and len(entry["normalized_trend"]) > 1:
            X.append(entry["normalized_trend"][:-1])  # Features: All years except the last
            y.append(entry["normalized_trend"][-1])  # Target: The last year population

    return np.array(X), np.array(y)

# Load Train & Test Data
X_train, y_train = load_biodiversity_data("data/biodiversity/train/biodiversity_loss_train.json")
X_test, y_test = load_biodiversity_data("data/biodiversity/test/biodiversity_loss_test.json")

# Reshape for LSTM (samples, time steps, features)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Define LSTM Model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    LSTM(50),
    Dense(1, activation="linear")
])

# Compile Model
model.compile(optimizer="adam", loss="mse")

# Train Model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Save Model
model.save("models/biodiversity_model.h5")
print(" Biodiversity loss model trained & saved successfully!")
