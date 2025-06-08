import xml.etree.ElementTree as ET

# === CONFIGURATION ===
xml_file = "20210325T1530Z_1D_NL_EQ_001.xml"

# --- CIM namespace ---
ns = {
    "cim": "http://iec.ch/TC57/CIM100#"
}

# === PARSE XML ===
tree = ET.parse(xml_file)
root = tree.getroot()

# === INITIALIZE TOTAL CAPACITY COUNTER ===
total_capacity_mw = 0.0

# === EXTRACT GENERATOR CAPACITIES ===
print("Generators and their maxOperatingP values:\n")

for generator in root.findall(".//cim:GeneratingUnit", ns):
    max_p = generator.find("cim:GeneratingUnit.maxOperatingP", ns)
    name = generator.find("cim:IdentifiedObject.name", ns)

    if max_p is not None:
        try:
            value = float(max_p.text)
            label = name.text if name is not None else "Unnamed Generator"
            print(f"• {label}: {value} MW")
            total_capacity_mw += value
        except ValueError:
            print("• Skipped one generator due to invalid maxOperatingP value.")

# === OUTPUT TOTAL CAPACITY ===
print(f"\nTOTAL PRODUCTION CAPACITY: {total_capacity_mw:.2f} MW")
