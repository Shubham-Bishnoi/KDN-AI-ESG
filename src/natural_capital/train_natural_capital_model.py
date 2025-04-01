import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Load & Preprocess Real Company Land-Use Data (CSV)
def load_land_use_data(csv_file):
    if not os.path.exists(csv_file):
        print(f" Error: File {csv_file} not found!")
        return None

    df = pd.read_csv(csv_file)

    # Check for necessary columns
    required_columns = {'land_area', 'land_type', 'biodiversity_index', 'carbon_sequestration', 'economic_value'}
    if not required_columns.issubset(df.columns):
        print(f" Error: Dataset is missing required columns: {required_columns - set(df.columns)}")
        return None

    # Convert Categorical Data to Numerical
    land_type_mapping = {"Forest": 1, "Wetland": 2, "Agricultural": 3, "Urban": 4}
    df['land_type'] = df['land_type'].map(land_type_mapping)

    # Normalize Data (Min-Max Scaling)
    df[['land_area', 'biodiversity_index', 'carbon_sequestration', 'economic_value']] = df[
        ['land_area', 'biodiversity_index', 'carbon_sequestration', 'economic_value']
    ].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    return df

# Train AI Model for Natural Capital Valuation
def train_natural_capital_model():
    csv_file = "data/land_use/organization_land_use.csv"
    df = load_land_use_data(csv_file)

    if df is None:
        return

    # AI Training Data
    X = df[['land_area', 'land_type', 'biodiversity_index', 'carbon_sequestration']].values
    y = df['economic_value'].values  # Target: Natural Capital Economic Value

    # Split into Train & Test Sets (80% Train, 20% Test)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build AI Model
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='linear')  # Output: Economic Value ($)
    ])

    # Compile Model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Train Model
    print(" Training Natural Capital Valuation Model...")
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    # Save Model
    os.makedirs("models", exist_ok=True)
    model.save("models/natural_capital_model.h5")
    print(" AI Model Trained & Saved for Natural Capital Valuation")

# Train Model
if __name__ == "__main__":
    train_natural_capital_model()
