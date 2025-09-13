import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# ---------------------------
# CONFIG
# ---------------------------
ITEM_TO_PREDICT = "Pizza"  # 🔁 Change to "Burger", "Coke", etc.
INPUT_CSV = "data/processed/final_data.csv"
MODEL_DIR = "models"
PLOT_DIR = "plots"

# ---------------------------
# Load & Preprocess Data
# ---------------------------
print(f"📥 Loading enriched dataset from {INPUT_CSV}...")
df = pd.read_csv(INPUT_CSV)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Filter one item
df = df[df["item_name"] == ITEM_TO_PREDICT]

# Aggregate by hour
df_hourly = df.groupby(pd.Grouper(key="timestamp", freq="H")).agg({
    "quantity": "sum"
}).reset_index()

# Fill missing hours
df_hourly = df_hourly.set_index("timestamp").asfreq("H", fill_value=0).reset_index()

# Prepare for Prophet
df_prophet = df_hourly.rename(columns={"timestamp": "ds", "quantity": "y"})

# ---------------------------
# Train Prophet Model
# ---------------------------
print("🧠 Training Prophet model...")
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=True,
    daily_seasonality=True
)
model.fit(df_prophet)

# ---------------------------
# Make Future Forecast
# ---------------------------
print("🔮 Forecasting next 24 hours...")
future = model.make_future_dataframe(periods=24, freq="H")
forecast = model.predict(future)

# ---------------------------
# Plot Forecast
# ---------------------------
os.makedirs(PLOT_DIR, exist_ok=True)
plot_path = f"{PLOT_DIR}/{ITEM_TO_PREDICT}_forecast.png"

fig = model.plot(forecast)
plt.title(f"{ITEM_TO_PREDICT} Demand Forecast (Next 24 Hours)")
plt.savefig(plot_path)
plt.close()

print(f"📈 Forecast saved: {plot_path}")
