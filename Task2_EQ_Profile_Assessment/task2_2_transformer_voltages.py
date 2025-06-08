import xml.etree.ElementTree as ET

# === CONFIGURATION ===
xml_file = "20210325T1530Z_1D_NL_EQ_001.xml"
target_id = "_2184f365-8cd5-4b5d-8a28-9d68603bb6a4"

# CIM + RDF namespaces for element access
ns = {
    "cim": "http://iec.ch/TC57/CIM100#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

# === PARSE XML ===
tree = ET.parse(xml_file)
root = tree.getroot()

# === FIND WINDINGS OF TARGET TRANSFORMER ===
print(f"Nominal voltages for transformer {target_id}:\n")

for winding in root.findall(".//cim:PowerTransformerEnd", ns):
    ref = winding.find("cim:PowerTransformerEnd.PowerTransformer", ns)
    if ref is None:
        continue

    ref_id = ref.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")
    if ref_id != f"#{target_id}":
        continue

    voltage = winding.find("cim:PowerTransformerEnd.ratedU", ns)
    name = winding.find("cim:IdentifiedObject.name", ns)

    print("Winding:", name.text if name is not None else "(Unnamed)")
    print("Voltage (kV):", voltage.text if voltage is not None else "?")
    print()
