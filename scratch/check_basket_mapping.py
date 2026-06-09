import pandas as pd
import sys

customer = pd.read_csv("data/ci_clustered.csv")
basket = pd.read_csv("data/customer_basket.csv")

print("customer shape:", customer.shape)
print("basket shape:", basket.shape)
print("customer_id min/max in customer:", customer['customer_id'].min(), customer['customer_id'].max())
print("customer_id min/max in basket:", basket['customer_id'].min(), basket['customer_id'].max())

merged = pd.merge(basket, customer, on="customer_id", how="inner")
print("merged shape:", merged.shape)

print("\nVegans top items in merged:")
vegans = merged[merged['final_cluster_label'] == 'Vegans']
# count items for vegans
items = []
for l in vegans['list_of_goods']:
    items.extend([i.strip() for i in l[1:-1].split(',') if i.strip() != "''"])
print(pd.Series(items).value_counts().head(10))

print("\nKarens top items in merged:")
karens = merged[merged['final_cluster_label'] == 'Karens']
items = []
for l in karens['list_of_goods']:
    items.extend([i.strip() for i in l[1:-1].split(',') if i.strip() != "''"])
print(pd.Series(items).value_counts().head(10))
