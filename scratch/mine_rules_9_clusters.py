import os
import sys
import json
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.basket import generate_association_rules

print("Mining association rules for the 9-cluster K-Means solution...")

# 1. Load data
customer_df = pd.read_csv('data/ci_clustered.csv')
basket_df = pd.read_csv('data/customer_basket.csv')

print(f"Loaded {len(customer_df)} customers and {len(basket_df)} baskets.")

# 2. Define parameters by cluster name
# Note: we use "Average customer" to match the CSV's label, but map it to "Average customers" parameters
params_by_cluster = {
    "Loyal big spenders": {
        "min_support": 0.02,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Clean and healthy": {
        "min_support": 0.02,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Average customer": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Bargain hunters": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Big families (big spenders)": {
        "min_support": 0.008,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Vegans": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    },
    "Tech enthusiasts": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    },
    "Karens": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    },
    "Gamers": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    }
}

# 3. Correct mapping of final_cluster_nr to final_cluster_label in CSV:
# 0: Bargain hunters
# 1: Tech enthusiasts
# 2: Big families (big spenders)
# 3: Clean and healthy
# 4: Average customer
# 5: Gamers
# 6: Loyal big spenders
# 7: Karens
# 8: Vegans
nr_to_label = {
    0: 'Bargain hunters',
    1: 'Tech enthusiasts',
    2: 'Big families (big spenders)',
    3: 'Clean and healthy',
    4: 'Average customer',
    5: 'Gamers',
    6: 'Loyal big spenders',
    7: 'Karens',
    8: 'Vegans'
}

# 4. Mine rules for each cluster number
output_rules = {}

for cluster_id, label in nr_to_label.items():
    print(f"\n--- Processing Cluster {cluster_id} ({label}) ---")
    cluster_customers = customer_df[customer_df['final_cluster_nr'] == cluster_id]
    params = params_by_cluster[label]
    
    print(f"Number of customers in cluster: {len(cluster_customers)}")
    print(f"Parameters: support={params['min_support']}, confidence={params['min_confidence']}")
    
    # Generate rules
    rules_df = generate_association_rules(
        customers=cluster_customers,
        basket=basket_df,
        min_support=params["min_support"],
        min_threshold=params["min_threshold"],
        min_confidence=params["min_confidence"]
    )
    
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
            
    output_rules[str(cluster_id)] = formatted_rules
    print(f"Mined {len(formatted_rules)} rules for cluster {cluster_id}.")

# 5. Save to JSON
output_path = 'data/cluster_association_rules.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_rules, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully generated and saved all rules to {output_path}!")
