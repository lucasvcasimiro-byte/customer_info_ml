import json

notebook_path = "notebooks/segmentation_fixed.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i in range(45, len(nb["cells"])):
    cell = nb["cells"][i]
    source = "".join(cell.get("source", []))
    print(f"\n=== Cell {i} ({cell['cell_type']}) ===")
    print("Source:")
    print(source[:1200] + ("..." if len(source) > 1200 else ""))
    
    if "outputs" in cell:
        for out in cell["outputs"]:
            if "text" in out:
                print("Output text:")
                print("".join(out["text"])[:1000])
            elif "data" in out and "text/plain" in out["data"]:
                print("Output plain data:")
                print("".join(out["data"]["text/plain"])[:1000])
