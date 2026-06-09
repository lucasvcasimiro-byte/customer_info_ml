import pandas as pd
import sys
import os
sys.path.append(os.path.abspath("."))
from functions.basket import generate_rules_for_all_clusters

print("Loading data...")
customer_basket = pd.read_csv("data/customer_basket.csv")
customer = pd.read_csv("data/ci_clustered.csv")

cluster_dataframes = {
    cluster: group
    for cluster, group in customer.groupby("final_cluster_label", sort=False)
}

params_by_cluster = {
    "Average customer": {"min_support": 0.05, "min_threshold": 1.0},
    "Bargain hunters": {"min_support": 0.03, "min_threshold": 1.0},
    "Big families (big spenders)": {"min_support": 0.01, "min_threshold": 1.5},
    "Clean and healthy": {"min_support": 0.01, "min_threshold": 1.0},
    "Gamers": {"min_support": 0.08, "min_threshold": 1.5},
    "Karens": {"min_support": 0.15, "min_threshold": 1.5},
    "Loyal big spenders": {"min_support": 0.02, "min_threshold": 1.0},
    "Tech enthusiasts": {"min_support": 0.03, "min_threshold": 1.5},
    "Vegans": {"min_support": 0.05, "min_threshold": 1.0},
}

all_rules = generate_rules_for_all_clusters(cluster_dataframes, customer_basket, params_by_cluster)

print("\n--- Karens Rules ---")
if "Karens" in all_rules and not all_rules["Karens"].empty:
    print(all_rules["Karens"].head())
else:
    print("No rules or empty")
    
print("\n--- Vegans Rules ---")
if "Vegans" in all_rules and not all_rules["Vegans"].empty:
    print(all_rules["Vegans"].head())
else:
    print("No rules or empty")
