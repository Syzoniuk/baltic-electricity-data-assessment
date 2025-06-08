import xml.etree.ElementTree as ET

# === CONFIGURATION ===
xml_file = "20210325T1530Z_1D_NL_EQ_001.xml"  # EQ-файл (может быть и SSH)

ns = {
    "cim": "http://iec.ch/TC57/CIM100#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

# === PARSE XML ===
tree = ET.parse(xml_file)
root = tree.getroot()

# === PROCESS: Find voltage-regulating controls and map to SynchronousMachine ===

# Step 1: Find all RegulatingControl with mode = voltage → map Terminal ID
voltage_terminals = set()
for rc in root.findall(".//cim:RegulatingControl", ns):
    mode = rc.find("cim:RegulatingControl.mode", ns)
    terminal = rc.find("cim:RegulatingControl.Terminal", ns)
    if mode is not None and "voltage" in mode.attrib.get(f"{{{ns['rdf']}}}resource", ""):
        if terminal is not None:
            ref = terminal.attrib.get(f"{{{ns['rdf']}}}resource", "")
            voltage_terminals.add(ref.split("#")[-1])

# Step 2: Find Terminal → ConductingEquipment link
terminal_to_equipment = {}
for terminal in root.findall(".//cim:Terminal", ns):
    term_id = terminal.attrib.get(f"{{{ns['rdf']}}}ID", "")
    if term_id in voltage_terminals:
        ce = terminal.find("cim:Terminal.ConductingEquipment", ns)
        if ce is not None:
            ref = ce.attrib.get(f"{{{ns['rdf']}}}resource", "")
            terminal_to_equipment[term_id] = ref.split("#")[-1]

# Step 3: Check if equipment is a SynchronousMachine
slack_candidates = []
for sm in root.findall(".//cim:SynchronousMachine", ns):
    sm_id = sm.attrib.get(f"{{{ns['rdf']}}}ID", "")
    sm_name = sm.findtext("cim:IdentifiedObject.name", default="(Unnamed)", namespaces=ns)
    if sm_id in terminal_to_equipment.values():
        slack_candidates.append((sm_id, sm_name))

# === OUTPUT ===
if slack_candidates:
    print("Likely Slack Generator via voltage RegulatingControl:")
    for sm_id, sm_name in slack_candidates:
        print(f" - {sm_name} (ID: {sm_id})")
    print("\n Heuristic based on RegulatingControl.Terminal → Terminal.ConductingEquipment → SynchronousMachine.")
else:
    print("No voltage-regulated synchronous machines matched via heuristic.")
