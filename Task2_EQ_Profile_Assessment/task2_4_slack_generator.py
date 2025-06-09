import xml.etree.ElementTree as ET

# === CONFIGURATION ===
xml_file = "20210325T1530Z_1D_NL_EQ_001.xml"  # EQ или SSH-файл

# === NAMESPACES ===
ns = {
    "cim": "http://iec.ch/TC57/CIM100#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

# === PARSE XML ===
tree = ET.parse(xml_file)
root = tree.getroot()

# === STEP 1: Check for synchronousMachine.referencePriority ===
for sm in root.findall(".//cim:SynchronousMachine", ns):
    ref_priority = sm.find("cim:SynchronousMachine.referencePriority", ns)
    if ref_priority is not None and ref_priority.text and ref_priority.text.strip() == "1":
        name = sm.findtext("cim:IdentifiedObject.name", default="(Unnamed)", namespaces=ns)
        rdf_id = sm.attrib.get(f"{{{ns['rdf']}}}ID")
        print("Slack Generator via referencePriority:")
        print(f" - {name} (ID: {rdf_id})")
        exit()

# === STEP 2: Fallback – Check for GeneratingUnit.normalPF ===
for gu in root.findall(".//cim:GeneratingUnit", ns):
    norm_pf = gu.find("cim:GeneratingUnit.normalPF", ns)
    if norm_pf is not None and norm_pf.text and float(norm_pf.text.strip()) > 0.0:
        name = gu.findtext("cim:IdentifiedObject.name", default="(Unnamed)", namespaces=ns)
        rdf_id = gu.attrib.get(f"{{{ns['rdf']}}}ID")
        print("Slack Generator candidate via normalPF > 0.0:")
        print(f" - {name} (ID: {rdf_id})")
        exit()

# === STEP 3: Heuristic fallback via voltage RegulatingControl.Terminal → Terminal → SynchronousMachine ===
# 3.1: Collect Terminal IDs from RegulatingControl.mode = voltage
voltage_terminals = set()
for rc in root.findall(".//cim:RegulatingControl", ns):
    mode = rc.find("cim:RegulatingControl.mode", ns)
    terminal = rc.find("cim:RegulatingControl.Terminal", ns)
    if mode is not None and "voltage" in mode.attrib.get(f"{{{ns['rdf']}}}resource", ""):
        if terminal is not None:
            ref = terminal.attrib.get(f"{{{ns['rdf']}}}resource", "")
            voltage_terminals.add(ref.split("#")[-1])

# 3.2: Map Terminal → ConductingEquipment
terminal_to_equipment = {}
for terminal in root.findall(".//cim:Terminal", ns):
    term_id = terminal.attrib.get(f"{{{ns['rdf']}}}ID", "")
    if term_id in voltage_terminals:
        ce = terminal.find("cim:Terminal.ConductingEquipment", ns)
        if ce is not None:
            ref = ce.attrib.get(f"{{{ns['rdf']}}}resource", "")
            terminal_to_equipment[term_id] = ref.split("#")[-1]

# 3.3: Match SynchronousMachine with equipment IDs
slack_candidates = []
for sm in root.findall(".//cim:SynchronousMachine", ns):
    sm_id = sm.attrib.get(f"{{{ns['rdf']}}}ID", "")
    sm_name = sm.findtext("cim:IdentifiedObject.name", default="(Unnamed)", namespaces=ns)
    if sm_id in terminal_to_equipment.values():
        slack_candidates.append((sm_id, sm_name))

# === OUTPUT ===
if slack_candidates:
    print("Slack Generator identified via voltage RegulatingControl heuristic:")
    for sm_id, sm_name in slack_candidates:
        print(f" - {sm_name} (ID: {sm_id})")
    print("\nHeuristic: RegulatingControl.Terminal → Terminal → SynchronousMachine")
else:
    print("No Slack Generator found using any method.")
