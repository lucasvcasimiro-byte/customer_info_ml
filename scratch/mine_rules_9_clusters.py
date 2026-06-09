import os
import sys
import json
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.basket import generate_rules_for_all_clusters

print("Mining association rules with final notebook parameters and functions.basket...")

# 1. Load data
customer_df = pd.read_csv('data/ci_clustered.csv')
basket_df = pd.read_csv('data/customer_basket.csv')

print(f"Loaded {len(customer_df)} customers and {len(basket_df)} baskets.")

# 2. Merge data to prepare cluster transaction dataframes
merged_data = pd.merge(basket_df, customer_df, on="customer_id", how="inner")
print(f"Merged into {len(merged_data)} transaction rows.")

cluster_dataframes = {
    cluster: group
    for cluster, group in merged_data.groupby("final_cluster_label", sort=False)
}

# 3. Parameters from Cell 11 of basket.ipynb
params_by_cluster = {
    "Bargain hunters": {
        "min_support": 0.01, 
        "min_threshold": 1.0, 
        "min_confidence": 0.10
    },
    "Tech enthusiasts": {
        "min_support": 0.02, 
        "min_threshold": 1.5, 
        "min_confidence": 0.10
    },
    "Big families (big spenders)": {
        "min_support": 0.01, 
        "min_threshold": 1.5, 
        "min_confidence": 0.10
    },
    "Clean and healthy": {
        "min_support": 0.01, 
        "min_threshold": 1.0, 
        "min_confidence": 0.10
    },
    "Average customer": {
        "min_support": 0.03, 
        "min_threshold": 1.0, 
        "min_confidence": 0.10
    },
    "Gamers": {
        "min_support": 0.03, 
        "min_threshold": 1.5, 
        "min_confidence": 0.10
    },
    "Loyal big spenders": {
        "min_support": 0.02, 
        "min_threshold": 1.0, 
        "min_confidence": 0.10
    },
    "Karens": {
        "min_support": 0.08, 
        "min_threshold": 1.5, 
        "min_confidence": 0.10
    },
    "Vegans": {
        "min_support": 0.05, 
        "min_threshold": 1.0, 
        "min_confidence": 0.10
    }
}

# 4. Mine rules for all clusters using the basket.py function
all_cluster_rules_df = generate_rules_for_all_clusters(
    cluster_dataframes=cluster_dataframes,
    params_by_cluster=params_by_cluster
)

# Mapping from final_cluster_label to final_cluster_nr
label_to_nr = {
    'Bargain hunters': 0,
    'Tech enthusiasts': 1,
    'Big families (big spenders)': 2,
    'Clean and healthy': 3,
    'Average customer': 4,
    'Gamers': 5,
    'Loyal big spenders': 6,
    'Karens': 7,
    'Vegans': 8
}

output_rules = {}

for label, rules_df in all_cluster_rules_df.items():
    if label not in label_to_nr:
        print(f"Warning: Group '{label}' not found in cluster label mapping. Skipping.")
        continue
        
    cluster_id = str(label_to_nr[label])
    formatted_rules = []
    
    if not rules_df.empty:
        # Filter to strictly 1-to-1 association rules (single antecedent and single consequent)
        one_to_one = rules_df[
            rules_df['antecedents'].apply(lambda x: len(x) == 1) & 
            rules_df['consequents'].apply(lambda x: len(x) == 1)
        ]
        
        # Sort by lift descending and select top 50 rules
        sorted_rules = one_to_one.sort_values(by="lift", ascending=False)
        for _, row in sorted_rules.head(50).iterrows():
            formatted_rules.append({
                "antecedents": list(row["antecedents"]),
                "consequents": list(row["consequents"]),
                "support": float(row["support"]),
                "confidence": float(row["confidence"]),
                "lift": float(row["lift"])
            })
            
    output_rules[cluster_id] = formatted_rules
    print(f"Mined {len(formatted_rules)} rules for cluster {cluster_id} ({label}).")

# Initialize empty rules for any missing clusters
for i in range(9):
    cid = str(i)
    if cid not in output_rules:
        output_rules[cid] = []

# 5. Save to JSON
output_path = 'data/cluster_association_rules.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_rules, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully generated and saved all rules to {output_path}!")
