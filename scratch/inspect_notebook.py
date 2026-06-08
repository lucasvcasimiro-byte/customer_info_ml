import json

notebook_path = "notebooks/segmentation_fixed.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print("Cells count:", len(nb["cells"]))
for i, cell in enumerate(nb["cells"]):
    # Look for code cells that might have clustering, silhouette, or WCSS results
    source = "".join(cell.get("source", []))
    if any(keyword in source.lower() for keyword in ["silhouette", "wcss", "inertia", "scaler"]):
        print(f"\n--- Cell {i} ({cell['cell_type']}) ---")
        print("Source:")
        print(source[:500] + ("..." if len(source) > 500 else ""))
        
        # If there are outputs, let's print them
        if "outputs" in cell:
            for out in cell["outputs"]:
                if "text" in out:
                    print("Output text:")
                    print("".join(out["text"])[:800])
                elif "data" in out and "text/plain" in out["data"]:
                    print("Output plain data:")
                    print("".join(out["data"]["text/plain"])[:800])
