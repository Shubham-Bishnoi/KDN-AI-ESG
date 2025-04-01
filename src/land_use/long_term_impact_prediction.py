import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

# Load Data
data_path = "data/land_use/land_use_recommendations.csv"
if not os.path.exists(data_path):
    print(f" Error: {data_path} not found! Please generate recommendations first.")
    exit()

df = pd.read_csv(data_path)

# Select Relevant Features for Prediction
features = ["biodiversity_index", "carbon_sequestration", "economic_value"]
target = ["biodiversity_index", "carbon_sequestration", "economic_value"]  # Predict same metrics in the future

# Prepare Time-Series Data (Simulating 10 Years Future Impact)
def create_time_series(df, feature_columns, target_columns, time_steps=5):
    X, y = [], []
    for i in range(len(df) - time_steps):
        X.append(df[feature_columns].iloc[i: i + time_steps].values)
        y.append(df[target_columns].iloc[i + time_steps].values)
    return np.array(X), np.array(y)

# Normalize Data (Scaling Between 0-1)
from sklearn.preprocessing import MinMaxScaler
scalers = {}
for col in features:
    scalers[col] = MinMaxScaler()
    df[col] = scalers[col].fit_transform(df[[col]])

# Generate Training Data
time_steps = 5  # Use past 5 records to predict the next year
X, y = create_time_series(df, features, target, time_steps)

# Split into Train & Test Sets (80-20 Split)
split_index = int(len(X) * 0.8)
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# **LSTM Model for Long-Term Prediction**
model = Sequential([
    LSTM(64, activation='relu', return_sequences=True, input_shape=(time_steps, len(features))),
    Dropout(0.2),
    LSTM(32, activation='relu'),
    Dense(len(target), activation='linear')  # Multi-output: Predict Biodiversity, Carbon & Economic Value
])

# Compile Model
model.compile(optimizer='adam', loss='mse')
model.summary()

# Train Model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Save Model
model.save("models/long_term_impact_model.h5")
print(" AI Model Trained & Saved for Long-Term Impact Prediction")

# **Future Simulation: Predict Next 10 Years**
future_predictions = []
current_input = X[-1]  # Last known data

for _ in range(10):  # Predict for 10 years
    future_prediction = model.predict(current_input.reshape(1, time_steps, len(features)))
    future_predictions.append(future_prediction[0])
    
    # Shift Input & Append New Prediction
    current_input = np.roll(current_input, -1, axis=0)
    current_input[-1] = future_prediction[0]  # Replace last row with new prediction

# Convert Predictions to DataFrame
future_df = pd.DataFrame(future_predictions, columns=target)
for col in target:
    future_df[col] = scalers[col].inverse_transform(future_df[[col]])  # Convert Back to Original Scale

# Save Future Predictions
future_df.to_csv("data/land_use/long_term_predictions.csv", index=False)
print(" Future Predictions (Next 10 Years) Saved at: data/land_use/long_term_predictions.csv")
