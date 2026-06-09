import json
import pandas as pd
import sys

notebook_path = "notebooks/segmentation.ipynb"

# 1. Update the notebook safely
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        source = cell.get("source", [])
        if any("clusters_mapping = {" in line for line in source):
            # We found the cell, let's rewrite it
            new_source = [
                "# Mapping each cluster to its corresponding label\n",
                "# (Updated to conceptually match the basket outputs)\n",
                "clusters_mapping = {\n",
                "    0: 'Tech enthusiasts',\n",
                "    1: 'Clean and healthy',\n",
                "    2: 'Average customer',\n",
                "    3: 'Bargain hunters',\n",
                "    4: 'Gamers',\n",
                "    5: 'Karens',\n",
                "    6: 'Loyal big spenders',\n",
                "    7: 'Vegans',\n",
                "    8: 'Big families (big spenders)'}\n"
            ]
            cell["source"] = new_source
            print("Successfully updated segmentation.ipynb")
            break

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

# 2. Update ci_clustered.csv directly so they don't have to rerun the notebook
ci = pd.read_csv("data/ci_clustered.csv")

new_mapping = {
    0: 'Tech enthusiasts',
    1: 'Clean and healthy',
    2: 'Average customer',
    3: 'Bargain hunters',
    4: 'Gamers',
    5: 'Karens',
    6: 'Loyal big spenders',
    7: 'Vegans',
    8: 'Big families (big spenders)'
}

ci['final_cluster_label'] = ci['final_cluster_nr'].map(new_mapping)
ci.to_csv("data/ci_clustered.csv", index=False)
print("Successfully updated data/ci_clustered.csv")
