# task1_imbalance_activation_plot.py
# Author: Oleksandr Syzoniuk
# Description: Step 1 – Plot electricity imbalance data for the Baltic countries using the Transparency Dashboard API.

import requests
import pandas as pd
import matplotlib.pyplot as plt

# --- Settings for date range and selected countries ---
start = "2025-02-07T00:00"
end = "2025-02-11T00:00"
countries = ["Baltics", "Estonia", "Latvia", "Lithuania"]

# --- Function to fetch data from the Baltic Transparency API ---
def get_data(dataset_id, start, end):
    url = "https://api-baltic.transparency-dashboard.eu/api/v1/export"
    params = {
        "id": dataset_id,
        "start_date": start,
        "end_date": end,
        "output_time_zone": "EET",
        "output_format": "json",
        "json_header_groups": "0"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()["data"]
    times = [row["from"] for row in data["timeseries"]]
    values = [row["values"] for row in data["timeseries"]]
    columns = [col["group_level_0"] for col in data["columns"]]
    df = pd.DataFrame(values, columns=columns)
    df.index = pd.to_datetime(times)
    return df

# --- Load and filter imbalance data ---
imbalance = get_data("imbalance_volumes", start, end)
imbalance = imbalance[[c for c in countries if c in imbalance.columns]]

# --- Plot imbalance ---
plt.figure(figsize=(12, 6))
imbalance.plot(marker='o', linestyle='-')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.title("Electricity Imbalance (MWh)")
plt.ylabel("Imbalance")
plt.xlabel("Time")
plt.legend(title="Country")
plt.tight_layout()
plt.show()
