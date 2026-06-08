import json

notebook_path = "notebooks/segmentation_fixed.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

cell = nb["cells"][46]
print("Cell type:", cell["cell_type"])
print("Source:")
print("".join(cell["source"]))
print("\nOutputs:")
for out in cell["outputs"]:
    if "text" in out:
        print("".join(out["text"]))
    elif "data" in out and "text/plain" in out["data"]:
        print("".join(out["data"]["text/plain"]))
