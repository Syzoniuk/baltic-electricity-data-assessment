# task1_imbalance_activation_plot.py
# Author: Oleksandr Syzoniuk

import requests
import pandas as pd
import matplotlib.pyplot as plt
import pytz

# === CONFIGURATION ===
start_date = "2025-02-07T00:00"
end_date = "2025-02-11T00:00"
target_countries = ["Baltics", "Estonia", "Latvia", "Lithuania"]
timezone = "CET"  # or "EET", "UTC", etc.

# === FUNCTION: Fetch dataset from API ===
def fetch_dataset(dataset_id: str, start: str, end: str, tz: str) -> pd.DataFrame:
    url = "https://api-baltic.transparency-dashboard.eu/api/v1/export"
    params = {
        "id": dataset_id,
        "start_date": start,
        "end_date": end,
        "output_time_zone": tz,
        "output_format": "json",
        "json_header_groups": "0"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    json_data = response.json()["data"]

    timestamps = [entry["from"] for entry in json_data["timeseries"]]
    values = [entry["values"] for entry in json_data["timeseries"]]
    columns = [col["group_level_0"] for col in json_data["columns"]]

    df = pd.DataFrame(values, columns=columns)
    df.index = pd.to_datetime(timestamps).tz_convert(pytz.timezone(tz))
    return df

# === LOAD DATASETS ===
imbalance_df = fetch_dataset("imbalance_volumes", start_date, end_date, timezone)
activation_df = fetch_dataset("normal_activations_total", start_date, end_date, timezone)

# === FORMAT ACTIVATION COLUMNS ===
renamed_cols = []
col_counter = {}
for col in activation_df.columns:
    if col not in col_counter:
        col_counter[col] = 1
        renamed_cols.append(f"{col} | Upward")
    else:
        renamed_cols.append(f"{col} | Downward")
activation_df.columns = renamed_cols

# === FILTER ONLY TARGET COUNTRIES ===
imbalance_df = imbalance_df[[c for c in target_countries if c in imbalance_df.columns]]
activation_df = activation_df[[col for col in activation_df.columns if col.split(" | ")[0] in target_countries]]
activation_df = activation_df.apply(pd.to_numeric, errors='coerce')

# === ALIGN X-AXIS VISUALLY ===
shared_xlim = [
    min(imbalance_df.index.min(), activation_df.index.min()),
    max(imbalance_df.index.max(), activation_df.index.max())
]

# === PLOTTING ===
fig, (ax_imbalance, ax_activations) = plt.subplots(2, 1, figsize=(16, 9), constrained_layout=True)

# --- Plot 1: Imbalance ---
imbalance_df.plot(ax=ax_imbalance, linestyle='-', marker='o')
ax_imbalance.set_title("Electricity Imbalance (MWh)")
ax_imbalance.set_ylabel("Imbalance")
ax_imbalance.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax_imbalance.legend(title="Country")
ax_imbalance.set_xlim(shared_xlim)

# --- Plot 2: Activations ---
has_data = False
for col in activation_df.columns:
    data = activation_df[col].dropna()
    if not data.empty:
        linestyle = '--' if "Downward" in col else ':'
        marker = 'x' if "Downward" in col else 'o'
        ax_activations.plot(data.index, data.values, linestyle=linestyle, marker=marker, label=col)
        has_data = True

ax_activations.set_title("Normal Activations – Selected Countries")
ax_activations.set_ylabel("Activation (MW)")
ax_activations.set_xlabel(f"Time ({timezone})")
ax_activations.set_xlim(shared_xlim)

if not has_data:
    for country in target_countries:
        ax_activations.plot([], [], linestyle=':', marker='o', label=f"{country} | Upward")
        ax_activations.plot([], [], linestyle='--', marker='x', label=f"{country} | Downward")

ax_activations.legend(loc="upper right", ncol=2)

plt.show()
