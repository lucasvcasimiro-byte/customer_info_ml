import json

notebook_path = "notebooks/segmentation_fixed.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    source = "".join(cell.get("source", []))
    if "silhouette" in source.lower():
        print(f"\n=== Cell {i} ===")
        print(source[:500])
        if "outputs" in cell:
            for out in cell["outputs"]:
                if "text" in out:
                    print("".join(out["text"])[:800])
                elif "data" in out and "text/plain" in out["data"]:
                    print("".join(out["data"]["text/plain"])[:800])
