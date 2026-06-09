import pandas as pd

customer = pd.read_csv("data/ci_clustered.csv")

share_cols = [c for c in customer.columns if c.startswith('share_')]
cols = share_cols + ['number_complaints']

grouped = customer.groupby("final_cluster_label")[cols].mean().round(3)
print(grouped.T)
