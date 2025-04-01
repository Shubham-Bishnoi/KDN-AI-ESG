import pandas as pd
import numpy as np
import os

# Ensure data directory exists
data_path = "data/land_use/"
os.makedirs(data_path, exist_ok=True)

# Load the dataset
csv_file = os.path.join(data_path, "organization_land_use.csv")
output_file = os.path.join(data_path, "land_use_recommendations.csv")

if not os.path.exists(csv_file):
    print(f" Error: {csv_file} not found! Please ensure the dataset is in the correct location.")
    exit()

df = pd.read_csv(csv_file)

# Define recommendation rules
def recommend_land_use(row):
    land_type = row["land_type"]
    biodiversity_index = row["biodiversity_index"]
    carbon_sequestration = row["carbon_sequestration"]
    economic_value = row["economic_value"]

    recommendations = []

    # Rule 1: High biodiversity areas should be conserved
    if biodiversity_index > 0.8:
        recommendations.append("Conservation & Protection Initiatives")
    
    # Rule 2: Urban areas should have more green spaces
    if land_type == "Urban":
        recommendations.append("Green Infrastructure Development (Parks, Rooftop Gardens)")
    
    # Rule 3: Low biodiversity areas should be restored
    if biodiversity_index < 0.4:
        recommendations.append("Reforestation or Wetland Restoration")
    
    # Rule 4: High carbon sequestration lands should be protected
    if carbon_sequestration > 50:
        recommendations.append("Forest & Carbon Offset Protection Programs")

    # Rule 5: Low carbon sequestration areas should implement carbon offsetting
    if carbon_sequestration < 10:
        recommendations.append("Adopt Carbon Offset Programs (Afforestation, Biochar)")
    
    # Rule 6: If economic value is high, balance sustainability with economic incentives
    if economic_value > 100000:
        recommendations.append("Sustainable Agriculture & Eco-Tourism Development")

    return "; ".join(recommendations) if recommendations else "No Specific Recommendation"

# Apply recommendations to the dataset
df["recommendations"] = df.apply(recommend_land_use, axis=1)

# Save the recommendations to a new CSV file
df.to_csv(output_file, index=False)

print(f" Sustainable Land-Use Recommendations Generated and saved at: {output_file}")
