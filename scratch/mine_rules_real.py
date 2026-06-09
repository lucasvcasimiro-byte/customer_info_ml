import os
import sys
import json
import pandas as pd

# Add project root to sys.path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.basket import generate_rules_for_all_clusters

print("Running real rule mining using functions.basket...")

# 1. Load pre-clustered customers and shopping baskets
customer_df = pd.read_csv('data/ci_clustered.csv')
basket_df = pd.read_csv('data/customer_basket.csv')

print(f"Loaded {len(customer_df)} clustered customers and {len(basket_df)} shopping baskets.")

# 2. Define cluster dataframes as in basket.ipynb
cluster_dataframes = {
    cluster: group
    for cluster, group in customer_df.groupby("final_cluster_label")
}

# 3. Parameters from basket.ipynb
params_by_cluster = {
    "Loyal core spenders": {
        "min_support": 0.02,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Vegans": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Bargain hunters": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Karens": {
        "min_support": 0.008,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Tech enthusiasts": {
        "min_support": 0.006,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Big families (big spenders)": {
        "min_support": 0.006,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Gamers": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    }
}

# 4. Generate association rules using their exact generate_rules_for_all_clusters function
all_cluster_rules_df = generate_rules_for_all_clusters(
    cluster_dataframes=cluster_dataframes,
    basket=basket_df,
    params_by_cluster=params_by_cluster
)

# Mapping from final_cluster_label to final_cluster_nr
label_to_nr = {
    "Vegans": 0,
    "Loyal core spenders": 1,
    "Big families (big spenders)": 2,
    "Bargain hunters": 3,
    "Gamers": 4,
    "Karens": 5,
    "Tech enthusiasts": 6
}

# Convert results to the JSON structure expected by the server
output_rules = {}

for label, rules_df in all_cluster_rules_df.items():
    cluster_id = str(label_to_nr[label])
    formatted_rules = []
    
    if not rules_df.empty:
        # Sort by lift descending
        sorted_rules = rules_df.sort_values(by="lift", ascending=False)
        for _, row in sorted_rules.head(50).iterrows():
            formatted_rules.append({
                "antecedents": list(row["antecedents"]),
                "consequents": list(row["consequents"]),
                "support": float(row["support"]),
                "confidence": float(row["confidence"]),
                "lift": float(row["lift"])
            })
            
    output_rules[cluster_id] = formatted_rules
    print(f"Mined {len(formatted_rules)} rules for cluster {cluster_id} ({label})")

# 5. Save rules to JSON file
output_path = 'data/cluster_association_rules.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_rules, f, ensure_ascii=False, indent=2)

print(f"Mined rules saved successfully to {output_path}!")
