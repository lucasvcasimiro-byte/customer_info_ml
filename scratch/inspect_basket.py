import json

notebook_path = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\notebooks\basket.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if any(term in source for term in ['read_csv', 'cluster', 'ci_clustered', 'final_cluster', 'k=']):
            print(f"=== Cell {i} ===")
            print("\n".join(source.split("\n")[:15]))
            print("-" * 20)
