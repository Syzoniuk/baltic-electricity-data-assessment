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

### Thought Process & Tooling

To ensure clarity and modularity, I broke the task into data fetching, filtering, alignment, and plotting stages. Here’s why I chose each tool:

| Tool          | Role                                        | Rationale                                               |
|---------------|---------------------------------------------|----------------------------------------------------------|
| `requests`    | Fetch JSON datasets via API                 | Lightweight and standard for REST APIs                   |
| `pandas`      | Handle tabular data and time-series         | Ideal for reshaping electricity data chronologically     |
| `matplotlib`  | Create flexible subplots and legends        | Widely used, highly customizable plotting library        |
| `pytz`        | Convert timestamps into target timezones    | Ensures correct CET time alignment across both datasets  |

> ⚠️ I used `pytz` to match the timezone of the API output (`CET`) and to prevent misaligned timestamps when plotting activations and imbalances together.

---

###  Final Output – Visualizations

###  Figure 1 – 2025-02-07 to 2025-02-11

![Figure 1](Task1_Imbalance_Analysis/images/imbalance_activation_2025.png)

During this required period, the **“Baltics” aggregate column is empty** in the Transparency Dashboard data.  
So, I plotted individual countries — **Estonia, Latvia, and Lithuania** — to show granular insights.

This approach keeps the structure intact and ensures full visibility. The legend includes placeholders for both activation types (upward/downward), even when activation data is absent.

---

### Figure 2 – 2024-02-07 to 2024-02-11 (Test)

![Figure 2](Task1_Imbalance_Analysis/images/imbalance_activation_2024.png)

This test run confirms that the **plotting logic and dataset parsing work correctly**.  
Here, upward and downward activation data are available. They are plotted with dashed/solid lines and marker distinctions to maintain visual clarity.

---

### Analysis – Answer to Task Part 4

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

### 📁 Project Files (Task 1)

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

## 🧮 Task 2.1 – Total Generator Capacity

---

> **Objective:**  
Extract and calculate the **total production capacity** of all generators modeled in the provided CGMES EQ profile XML file.

---

### Thought Process & Tooling

This task focuses on **static power system modeling** via the EQ (Equipment) profile in CIM/XML format. I chose to directly parse the XML with Python’s `xml.etree.ElementTree`, as it’s lightweight and sufficient for structured CIM data when no inference or semantic layer is needed.

The script follows a simple logic:
1. Locate all `<cim:GeneratingUnit>` elements.
2. Read each unit’s `maxOperatingP` value.
3. Sum the values to determine **total production capacity** in megawatts (MW).

---

### Result Summary – Answer to Task 2.1

The script parsed all generating units and extracted their declared maximum active power output. The final output displays:

- Each generator’s name (if available) and capacity in MW.
- A total summation of available generation capacity across the modeled system.

---

## 🔌 Task 2.2 – Transformer Winding Voltages

---

> **Objective:**  
Identify and extract the **rated voltages** for each winding of a specific transformer (by ID) from the CGMES EQ profile XML.

---

###  Thought Process & Tooling

We focus here on a specific transformer with ID `_2184f365-8cd5-4b5d-8a28-9d68603bb6a4`.  
The logic follows these steps:

1. Search all `<cim:PowerTransformerEnd>` elements.
2. Match those linked to the correct transformer via the RDF reference.
3. Extract each winding’s `ratedU` and name (if available).

Namespaces used:

- `cim`: CIM standard for equipment metadata.
- `rdf`: Used for referencing transformer relationships via IDs.

---

###  Result Summary – Answer to Task 2.2

The script successfully identified and printed the **rated voltages (in kV)** for each winding of the transformer.  
It lists all connected windings, their names, and their voltage ratings.

Winding: NL_TR2_2 <br>
Voltage (kV): 220

Winding: NL_TR2_2 <br>
Voltage (kV): 15.75





## ⚡ Task 2.3 – Current Limits for Line: NL-Line_5

---

> **Objective:**  
Extract the **current limit values (Amperes)** for a specific transmission line – `NL-Line_5` – from the provided CGMES EQ profile.

---

###  Thought Process & Tooling

This task focuses on understanding how operational limits are **linked across different CIM elements**:
- First, I locate `OperationalLimitSet` blocks where the description contains the target line name (`NL-Line_5`).
- Then, I extract all `CurrentLimit` entries referencing those sets.

The XML is parsed using `xml.etree.ElementTree`, and namespace handling ensures accurate access to nested RDF/CIM elements.

---

###  Result Summary – Answer to Task 2.3

The script produced the following output:

  Limit Type  Normal Value (A) <br>
0       PATL            1876.0 <br>
1       TATL             500.0 <br>
2       PATL            1876.0 <br>
3       TATL             500.0 <br>

---
In CGMES EQ profiles, transmission lines can have two distinct current limits:

- **PATL** – *Permanently Admissible Transmission Limit*  
  This is the **maximum continuous current** the line can carry under normal conditions.  


- **TATL** – *Temporarily Admissible Transmission Limit*  
  This is a **higher current limit allowed only during emergencies or contingency situations**.  

### Difference

| Type | Condition | Duration | Purpose |
|------|-----------|----------|---------|
| PATL | Normal operation | Unlimited | Safe long-term operation |
| TATL | Emergency use only | Limited time | Short-term overload capability |



## ⚡ Task 2.4 – Slack Generator Identification

---

> **Objective:**  
Determine which generator is used as the **slack** in the provided CGMES model, based on structural indicators available in the EQ profile.

---

### 🧠 Thought Process & Heuristic Strategy

In CGMES-compliant systems, the slack generator is typically defined using the following hierarchy:

1. `SynchronousMachine.referencePriority = 1` → official CGMES marker [1]  
2. `GeneratingUnit.normalPF > 0` → used for distributed slack participation [1]  
3. `TopologicalIsland.AngleRefTopologicalNode` → used when SV profiles are available [1]

In this model: 
- The `referencePriority` tag was missing  
- No `normalPF` attributes were available

As described in [1], when multiple generators have `referencePriority = 1`, the slack is distributed using `normalPF`. When none of these tags exist, the model cannot be interpreted using formal CGMES rules.

Therefore, I applied a **structured fallback heuristic** based on CGMES linkage rules [2] and system modeling principles discussed in [3]:

1. I first searched for `RegulatingControl` blocks set to `mode = voltage`, as these are typically used to regulate bus voltage — a role often fulfilled by slack generators in simulation environments [2].

2. From each voltage-mode control, I followed the linked `Terminal`.

3. From each `Terminal`, I traced the associated `ConductingEquipment`, leading to connected `SynchronousMachine` elements [2].

4. Only one generator — `NL-G1` — was uniquely linked through this voltage-regulation structure.

Based on this structural chain and the absence of standard slack indicators, I concluded that `NL-G1` was most likely intended as the slack generator in this model.

---

###  Result Summary – Answer to Task 2.4

The script successfully identified the following generator based on structural links:

- **Likely Slack Generator:** `NL-G1`  
- **CGMES ID:** `_9c3b8f97-7972-477d-9dc8-87365cc0ad0e`  
- **Reasoning:** This generator is connected via terminal to a `RegulatingControl` object operating in `voltage` mode

> ⚠️ This is a heuristic result, not a formally defined slack unit per CGMES. It is used only when standard slack markers are absent [1], [2].

---

### 📚 References

[1] ENTSO-E, *Implementation Guide for CGMES 2.4.15*, March 2016.  
https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/160315_ImplementationGuide_CGMES_2_4_15.pdf

[2] IEC TC57, *Technical Specification for CGMES 2.5 – Part 1 (IEC 61970-600 Ed2)*, 2016.  
https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/IOP/CGMES_2_5_TechnicalSpecification_61970-600_Part%201_Ed2.pdf

[3] S. V. Dhople, Y. C. Chen, A. Al-Digs, and A. Domínguez-García, “Reexamining the Distributed Slack Bus,” *IEEE Transactions on Power Systems*, vol. 35, no. 6, pp. 4894–4904, 2020.  
https://aledan.ece.illinois.edu/files/2020/04/TPWRS_2020a.pdf
