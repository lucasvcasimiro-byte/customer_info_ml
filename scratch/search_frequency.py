import json

notebook_path = "notebooks/segmentation_fixed.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    source = "".join(cell.get("source", []))
    if "frequency" in source.lower():
        print(f"Cell {i} contains 'frequency'")
