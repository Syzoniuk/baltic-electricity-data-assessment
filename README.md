# ⚡ Baltic Electricity Data Assessment

**Author:** Oleksandr Syzoniuk  
**Repository:** `baltic-electricity-data-assessment`  
**Date:** June 2025

---


## 📌 Navigation

- [Task 1 – Baltic Imbalance & Activation Analysis](#-task-1--baltic-imbalance--activation-analysis)
- [Task 2 – EQ Profile Model Assessment](#-task-2--eq-profile-model-assessment)
  - [Task 2.1 – Total Generator Capacity](#task-21--total-generator-capacity)
- [Task 3 – ... (Add when ready)](#)

---

## 🧭 Task 1 – Baltic Imbalance & Activation Analysis

1. Inherit data on **Baltic imbalance volumes**.
2. Inherit data on **activation volumes** (upward and downward).
3. Plot both datasets in one clear, well-labeled figure.
4. Analyze whether activation responses reduced imbalance during **2025-02-07 to 2025-02-11**.

---

## 🛠️ Thought Process & Tooling

To ensure clarity and modularity, I broke the task into data fetching, filtering, alignment, and plotting stages. Here’s why I chose each tool:

| Tool          | Role                                        | Rationale                                               |
|---------------|---------------------------------------------|----------------------------------------------------------|
| `requests`    | Fetch JSON datasets via API                 | Lightweight and standard for REST APIs                   |
| `pandas`      | Handle tabular data and time-series         | Ideal for reshaping electricity data chronologically     |
| `matplotlib`  | Create flexible subplots and legends        | Widely used, highly customizable plotting library        |
| `pytz`        | Convert timestamps into target timezones    | Ensures correct CET time alignment across both datasets  |

> ⚠️ I used `pytz` to match the timezone of the API output (`CET`) and to prevent misaligned timestamps when plotting activations and imbalances together.

---

## 📈 Final Output – Visualizations

### 🔹 Figure 1 – 2025-02-07 to 2025-02-11

![Figure 1](Task1_Imbalance_Analysis/images/imbalance_activation_2025.png)

During this required period, the **“Baltics” aggregate column is empty** in the Transparency Dashboard data.  
So, I plotted individual countries — **Estonia, Latvia, and Lithuania** — to show granular insights.

This approach keeps the structure intact and ensures full visibility. The legend includes placeholders for both activation types (upward/downward), even when activation data is absent.

---

### 🔹 Figure 2 – 2024-02-07 to 2024-02-11 (Test)

![Figure 2](Task1_Imbalance_Analysis/images/imbalance_activation_2024.png)

This test run confirms that the **plotting logic and dataset parsing work correctly**.  
Here, upward and downward activation data are available. They are plotted with dashed/solid lines and marker distinctions to maintain visual clarity.

---

## ✍️ Analysis – Answer to Task Part 4

Although the API did not contain valid data for the requested 2025-02-07 to 2025-02-11 period, I reproduced the same logic using the 2024-02-07 to 2024-02-11 window. This allows demonstration of the expected dynamics.

From the resulting figure:

- **Electricity imbalance** is plotted in the top graph, showing MWh deviations for Baltics and each country.
- **Activation events** are in the lower graph, split into upward/downward regulation.

We generally observe:

- **Upward activations** occur during **negative imbalances** (shortage of power), helping restore balance.
- **Downward activations** occur during **positive imbalances** (surplus of power), also aiming to stabilize the grid.

These patterns confirm the regulation system responds logically in most cases. While small timing mismatches can occur, the overall mechanism appears effective and well-aligned with imbalance signals — validating the adjustment activity logic.

In 2025, due to the absence of activation data, the second subplot is visually empty.  
However, the imbalance curves for individual countries are still visible and valuable for system insights.  
If the API had returned activation values, I would expect **corrective actions to imbalance spikes**, as demonstrated in 2024.

---

## 📁 Project Files (Task 1)

```
baltic-electricity-data-assessment/
├── task1_energy_analysis.py         # Final Python script
├── images/
│   ├── imbalance_activation_2025.png   # Required task period
│   └── imbalance_activation_2024.png   # Logic validation
└
```

---

## ⚙️ Task 2 – EQ Profile Model Assessment

This task group covers semantic and structural evaluations of CGMES-based equipment profiles used in power systems.  
Each sub-task examines specific elements of the EQ model — from generation capacity to transformer limits and data consistency.

---

### 🧮 Task 2.1 – Total Generator Capacity

---

## 🧭 Task Summary

> **Objective:**  
Extract and calculate the **total production capacity** of all generators modeled in the provided CGMES EQ profile XML file.

---

## 🛠️ Thought Process & Tooling

This task focuses on **static power system modeling** via the EQ (Equipment) profile in CIM/XML format. I chose to directly parse the XML with Python’s `xml.etree.ElementTree`, as it’s lightweight and sufficient for structured CIM data when no inference or semantic layer is needed.

The script follows a simple logic:
1. Locate all `<cim:GeneratingUnit>` elements.
2. Read each unit’s `maxOperatingP` value.
3. Sum the values to determine **total production capacity** in megawatts (MW).

> 🗂️ The input file was the official `20210325T1530Z_1D_NL_EQ_001.xml` EQ profile provided for this assignment.

---

## Result Summary – Answer to Task 2.1

The script parsed all generating units and extracted their declared maximum active power output. The final output displays:

- Each generator’s name (if available) and capacity in MW.
- A total summation of available generation capacity across the modeled system.

> 💡 This allows a clear, reproducible evaluation of production potential from the static network model.

---

## 📁 Project Files (Task 2)

```
baltic-electricity-data-assessment/
├── Task2_EQ_Profile_Assessment/
│   ├── task2_1_total_capacity.py             # Python script for total generator capacity
│   └── 20210325T1530Z_1D_NL_EQ_001.xml       # Input EQ profile XML file
```
