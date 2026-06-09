with open(r"notebooks/basket.ipynb", 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
# Let's search for keywords
keywords = ['ci_clustered', 'ci_clustering', 'kmeans', 'hierarchical', 'n_clusters', 'k=']
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")
    for m in matches[:5]:
        start = max(0, m - 40)
        end = min(len(content), m + 80)
        snippet = content[start:end].replace('\n', ' ')
        print(f"  Snippet: ... {snippet} ...")
