import json

notebook_path = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\notebooks\segmentation.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Let's search for cells containing "RobustScaler", "KMeans", "k=8", "vegetarian", "vegans"
for i, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if any(term in source for term in ['to_csv', 'final_cluster', 'KMeans', 'RobustScaler', 'vegetarian', 'vegans']):
            # Print cell index and snippet of code
            print(f"=== Cell {i} ===")
            print("\n".join(source.split("\n")[:15]))
            print("-" * 20)
