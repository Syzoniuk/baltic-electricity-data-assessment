from lxml import etree
import pandas as pd

# === CONFIGURATION ===
xml_file_path = "20210325T1530Z_1D_NL_EQ_001.xml"
target_line_name = "NL-Line_5"

# === PARSE XML ===
tree = etree.parse(xml_file_path)
root = tree.getroot()
nsmap = {
    'cim': "http://iec.ch/TC57/CIM100#",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

# === STEP 1: Find OperationalLimitSet IDs by line name in description ===
limit_set_ids = []
for elem in root.findall("cim:OperationalLimitSet", nsmap):
    desc = elem.find("cim:IdentifiedObject.description", nsmap)
    if desc is not None and target_line_name in desc.text:
        limit_set_ids.append(elem.get(f"{{{nsmap['rdf']}}}ID"))

# === STEP 2: Extract CurrentLimits for these OperationalLimitSets ===
limits = []
for elem in root.findall("cim:CurrentLimit", nsmap):
    ref = elem.find("cim:OperationalLimit.OperationalLimitSet", nsmap)
    if ref is not None:
        ref_id = ref.get(f"{{{nsmap['rdf']}}}resource").lstrip("#")
        if ref_id in limit_set_ids:
            name = elem.find("cim:IdentifiedObject.name", nsmap)
            value = elem.find("cim:CurrentLimit.normalValue", nsmap)
            limits.append((name.text if name is not None else "Unnamed", float(value.text)))

# === DISPLAY RESULTS ===
df = pd.DataFrame(limits, columns=["Limit Type", "Normal Value (A)"])
print(df)
