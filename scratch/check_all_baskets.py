import pandas as pd

info = pd.read_csv("data/customer_info.csv")
basket = pd.read_csv("data/customer_basket.csv")

top_fish_share_id = info.sort_values('share_fresh_fish', ascending=False).iloc[0]['customer_id']
print(f"Customer {top_fish_share_id} has the highest share_fresh_fish ({info.sort_values('share_fresh_fish', ascending=False).iloc[0]['share_fresh_fish']}).")

baskets_for_user = basket[basket['customer_id'] == top_fish_share_id]
print(f"They have {len(baskets_for_user)} baskets.")
for i, b in enumerate(baskets_for_user['list_of_goods']):
    print(f"Basket {i+1}: {b}")
