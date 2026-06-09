import json
import re

notebook_path = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas/customer_info_project/notebooks/basket.ipynb"

with open(notebook_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's extract cells that look like JSON code cells
# Since it is a Jupyter Notebook, let's load it using json if possible, or clean up bad quotes
try:
    nb = json.loads(content)
    print("Notebook loaded successfully as JSON!")
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            src = "".join(cell.get('source', []))
            if any(k in src for k in ['generate_rules', 'apriori', 'association_rules', 'params_by_cluster']):
                print(f"=== Cell {i} ===")
                print(src)
                print("="*50)
except Exception as e:
    print(f"JSON Load error: {e}. Let's do regex search instead.")
    # Search for code blocks or relevant lines
    for line in content.split('\n'):
        if any(k in line for k in ['generate_rules_for_all_clusters', 'params_by_cluster', 'min_support', 'association_rules']):
            print(line.strip()[:120])
