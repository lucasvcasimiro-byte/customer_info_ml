import pandas as pd

info = pd.read_csv("data/ci_clustered.csv")
basket = pd.read_csv("data/customer_basket.csv")

# Find a customer who buys a lot of fish in the basket
fish_items = ['fresh tuna', 'shrimp', 'salmon', 'catfish', 'seabass', 'canned_tuna']

basket['fish_count'] = basket['list_of_goods'].apply(lambda x: sum(1 for item in fish_items if item in x))

top_fish_buyer_id = basket.sort_values('fish_count', ascending=False).iloc[0]['customer_id']
print(f"Customer {top_fish_buyer_id} buys the most fish in basket.")

print("\nTheir basket:")
print(basket[basket['customer_id'] == top_fish_buyer_id]['list_of_goods'].iloc[0])

print("\nTheir spend shares in ci_clustered.csv:")
info_row = info[info['customer_id'] == top_fish_buyer_id].iloc[0]
print(info_row[['share_fish', 'share_vegetables', 'share_meat', 'number_complaints', 'final_cluster_label']])

# Now find a customer who has high share_fish in ci_clustered.csv
top_fish_share_id = info.sort_values('share_fish', ascending=False).iloc[0]['customer_id']
print(f"\n\nCustomer {top_fish_share_id} has the highest share_fish ({info.sort_values('share_fish', ascending=False).iloc[0]['share_fish']}).")
print("Their cluster is:", info[info['customer_id'] == top_fish_share_id].iloc[0]['final_cluster_label'])

print("\nTheir basket:")
b = basket[basket['customer_id'] == top_fish_share_id]
if not b.empty:
    print(b['list_of_goods'].iloc[0])
else:
    print("No basket found!")
