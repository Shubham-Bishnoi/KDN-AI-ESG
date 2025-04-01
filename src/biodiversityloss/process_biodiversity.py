import pandas as pd
import os
import json
import numpy as np

# Ensure directories exist
os.makedirs("data/biodiversity/train", exist_ok=True)
os.makedirs("data/biodiversity/test", exist_ok=True)
os.makedirs("data/biodiversity/processed", exist_ok=True)

# Path to the CSV file
csv_file = "data/biodiversity/biodiversity_loss.csv"

# Check if file exists
if os.path.exists(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Display the first few rows
    print("🔍 Preview of Biodiversity Data:")
    print(df.head())

    # Select relevant columns
    selected_columns = ['Binomial', 'Common_name', 'Country']  # Adjust based on available columns

    # Detect year-based population columns (e.g., 1970-2020)
    year_columns = [col for col in df.columns if col.isdigit()]  

    # Ensure at least some years exist
    if not year_columns:
        print(" Error: No year-based population columns found!")
    else:
        # Keep only necessary columns
        df = df[selected_columns + year_columns]

        # Fill missing population data using linear interpolation
        df[year_columns] = df[year_columns].interpolate(method='linear', axis=1).fillna(method='bfill').fillna(method='ffill')

        # Convert to JSON
        biodiversity_data = df.to_dict(orient='records')

        # Normalize population trends
        for record in biodiversity_data:
            values = [record[year] for year in year_columns]
            min_val, max_val = min(values), max(values)
            record["normalized_trend"] = [(val - min_val) / (max_val - min_val) if max_val != min_val else 0 for val in values]

        # Split into train & test
        train_data = biodiversity_data[:int(len(biodiversity_data) * 0.8)]
        test_data = biodiversity_data[int(len(biodiversity_data) * 0.8):]

        # Save Train Dataset
        with open("data/biodiversity/train/biodiversity_loss_train.json", "w") as f:
            json.dump(train_data, f)

        # Save Test Dataset
        with open("data/biodiversity/test/biodiversity_loss_test.json", "w") as f:
            json.dump(test_data, f)

        print("✅ Biodiversity loss train & test data processed successfully!")

else:
    print(f"Error: {csv_file} not found. Please ensure the dataset is in the correct location.")
