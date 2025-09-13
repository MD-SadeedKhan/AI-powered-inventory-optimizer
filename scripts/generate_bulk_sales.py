import csv
import random
from datetime import datetime, timedelta
import os

ITEMS = ["Burger", "Fries", "Coke", "Ice Cream", "Pizza", "Sandwich"]

def generate_bulk_sales(num_rows=1000):
    base_time = datetime.now() - timedelta(hours=24)
    rows = []

    for i in range(num_rows):
        time_offset = timedelta(seconds=random.randint(0, 86400))  # 24 hrs
        timestamp = (base_time + time_offset).strftime("%Y-%m-%d %H:%M:%S")
        item = random.choice(ITEMS)
        quantity = random.randint(1, 5)

        rows.append([timestamp, item, quantity])

    return sorted(rows, key=lambda x: x[0])  # sort by time

def save_to_csv(rows, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "item_name", "quantity"])
        writer.writerows(rows)

if __name__ == "__main__":
    output_path = "data/simulation/live_sales.csv"
    print("⚙️ Generating 1000 bulk sales transactions...")
    sales_rows = generate_bulk_sales(1000)
    save_to_csv(sales_rows, output_path)
    print(f"✅ Done! File saved at {output_path}")
