import json

with open("data/cluster_association_rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)
    
print("Keys in rules file:", list(rules.keys()))
for k, v in rules.items():
    print(f"Cluster {k} has {len(v)} rules")
