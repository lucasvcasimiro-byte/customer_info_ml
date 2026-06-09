import json
import re
import sys
import os
import matplotlib

# Use Agg backend to run headless without gui window popups
matplotlib.use('Agg')

print("Executing notebooks/segmentation.ipynb code cells...")

with open('notebooks/segmentation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Extract and clean code cells
compiled_code = []
for idx, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        # Remove magic commands like %matplotlib inline or %load_ext
        source_clean = re.sub(r'(?m)^%.*', '', source)
        compiled_code.append((idx, source_clean))

# Execute cells in order in a shared globals context
globals_dict = {
    'display': print,
    'print': print,
    '__name__': '__main__'
}

for idx, code in compiled_code:
    if not code.strip():
        continue
    # Skip any blocking interactive commands like plt.show()
    # (they are fine under Agg backend, but keeping it clean)
    try:
        exec(code, globals_dict)
    except Exception as e:
        print(f"Error in cell index {idx}: {e}")
        # Print a snippet of the code that failed
        print("Code snippet:")
        print("\n".join(code.split("\n")[:10]))
        sys.exit(1)

print("Notebook executed successfully and data/ci_clustered.csv was generated!")
