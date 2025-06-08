import xml.etree.ElementTree as ET

# === CONFIGURATION ===
xml_file = "20210325T1530Z_1D_NL_EQ_001.xml"
target_line_name = "NL-Line_5"

# === NAMESPACES ===
ns = {
    "cim": "http://iec.ch/TC57/CIM100#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

# === PARSE XML ===
tree = ET.parse(xml_file)
root = tree.getroot()

# === FIND OperationalLimitSet IDs for the given line ===
limit_set_ids = set()
for elem in root.findall(".//cim:OperationalLimitSet", ns):
    desc = elem.find("cim:IdentifiedObject.description", ns)
    if desc is not None and target_line_name in desc.text:
        rdf_id = elem.attrib.get(f"{{{ns['rdf']}}}ID")
        if rdf_id:
            limit_set_ids.add(f"#{rdf_id}")

# === FIND CurrentLimit entries that reference those sets ===
print(f"Current Limits for line: {target_line_name}\n")

if not limit_set_ids:
    print("No matching OperationalLimitSet found.\n")
else:
    found_any = False
    printed_names = set()  # ← Track printed limit types (e.g., PATL, TATL)

    for cl in root.findall(".//cim:CurrentLimit", ns):
        limit_ref = cl.find("cim:OperationalLimit.OperationalLimitSet", ns)
        if limit_ref is not None:
            ref_id = limit_ref.attrib.get(f"{{{ns['rdf']}}}resource")
            if ref_id in limit_set_ids:
                name_elem = cl.find("cim:IdentifiedObject.name", ns)
                value_elem = cl.find("cim:CurrentLimit.normalValue", ns)

                if name_elem is not None and value_elem is not None:
                    limit_name = name_elem.text
                    if limit_name not in printed_names:
                        print(f"Limit Name: {limit_name}")
                        print(f"Current Value (A): {value_elem.text}\n")
                        printed_names.add(limit_name)
                        found_any = True

    if not found_any:
        print("No CurrentLimit entries found for the target line.\n")

