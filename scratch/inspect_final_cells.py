import json

notebook_path = r"c:\Users\afons\OneDrive - NOVAIMS\2 ano 2 semestre\ML2\aulaspraticas\customer_info_project\notebooks\segmentation.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in range(50, 59):
    if i < len(nb.get('cells', [])):
        cell = nb['cells'][i]
        print(f"=== Cell {i} ({cell.get('cell_type')}) ===")
        source = "".join(cell.get('source', []))
        print(source)
        if cell.get('cell_type') == 'code' and cell.get('outputs'):
            print("--- Output ---")
            for output in cell['outputs'][:2]:
                if 'text' in output:
                    print("".join(output['text']))
                elif 'data' in output and 'text/plain' in output['data']:
                    print("".join(output['data']['text/plain']))
        print("=" * 40)
