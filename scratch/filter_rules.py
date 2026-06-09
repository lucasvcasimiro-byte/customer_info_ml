import json
import os

rules_file = 'data/cluster_association_rules.json'

if os.path.exists(rules_file):
    print("Loading rules...")
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    filtered_rules = {}
    total_original = 0
    total_filtered = 0

    for cluster_id, cluster_list in rules.items():
        total_original += len(cluster_list)
        filtered_list = []
        for rule in cluster_list:
            if len(rule['antecedents']) == 1 and len(rule['consequents']) == 1:
                filtered_list.append(rule)
        filtered_rules[cluster_id] = filtered_list
        total_filtered += len(filtered_list)

    print(f"Original rules: {total_original}")
    print(f"Filtered rules (1-to-1): {total_filtered}")

    with open(rules_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_rules, f, ensure_ascii=False, indent=2)

    print("Filtered rules saved successfully!")
else:
    print("Rules file not found!")
