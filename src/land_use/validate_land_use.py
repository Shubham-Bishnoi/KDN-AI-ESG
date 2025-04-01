import pandas as pd

# Load generated recommendations
df = pd.read_csv("data/land_use/land_use_recommendations.csv")

# Display sample recommendations
print(" Preview of Recommendations:")
print(df.sample(10))

# Check unique recommendations
print("\n Unique Recommendations Provided:")
print(df["recommendations"].value_counts())
