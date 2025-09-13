import pandas as pd
import requests
import holidays

# --------------------
# 1. Load the sales data
# --------------------
def load_sales_data(file_path):
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    return df

# --------------------
# 2. Add holiday flag
# --------------------
def add_holiday_column(df, country_code="IN"):
    india_holidays = holidays.CountryHoliday(country_code)
    df["is_holiday"] = df["date"].apply(lambda date: 1 if date in india_holidays else 0)
    return df

# --------------------
# 3. Add dummy weather (static or fetch from real API if needed)
# --------------------
def add_weather_column(df):
    # For now, simulate weather as a function of hour
    def temp_by_hour(h):
        if h < 6:
            return 20
        elif h < 12:
            return 28
        elif h < 18:
            return 35
        else:
            return 26
    df["temperature"] = df["hour"].apply(temp_by_hour)
    return df

# --------------------
# 4. Save enriched data
# --------------------
def save_enriched_data(df, out_path):
    df[["timestamp", "item_name", "quantity", "hour", "is_holiday", "temperature"]].to_csv(out_path, index=False)

if __name__ == "__main__":
    input_path = "data/simulation/live_sales.csv"
    output_path = "data/processed/final_data.csv"

    print("📥 Loading sales data...")
    df = load_sales_data(input_path)

    print("📅 Adding holiday info...")
    df = add_holiday_column(df)

    print("🌡️ Adding weather info...")
    df = add_weather_column(df)

    print(f"💾 Saving enriched data to {output_path}")
    save_enriched_data(df, output_path)
    print("✅ Enrichment complete.")
