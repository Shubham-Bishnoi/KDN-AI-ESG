import pandas as pd
import matplotlib.pyplot as plt

# Load Predictions
future_df = pd.read_csv("data/land_use/long_term_predictions.csv")

# Plot Trends
plt.figure(figsize=(12, 6))

for col in future_df.columns:
    plt.plot(range(1, 11), future_df[col], marker="o", label=col)

plt.xlabel("Years into Future")
plt.ylabel("Predicted Values")
plt.title(" Long-Term Impact of Sustainable Land-Use Changes")
plt.legend()
plt.grid()
plt.show()
