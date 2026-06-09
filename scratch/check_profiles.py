import pandas as pd
import sys
import os

print("Loading data...")
customer = pd.read_csv("data/ci_clustered.csv")

# Print average spend shares for Karens and Vegans
cols_to_check = ['share_vegetables', 'share_fresh_meat', 'share_fresh_fish', 'share_technology', 'number_complaints', 'share_baby_products']
cols = [c for c in cols_to_check if c in customer.columns]

grouped = customer.groupby("final_cluster_label")[cols].mean()
print("\n--- Average Characteristics by Cluster ---")
print(grouped)
