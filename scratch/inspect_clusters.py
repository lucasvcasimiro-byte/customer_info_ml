import pandas as pd
import json
import numpy as np

# Load the clustered dataset
df = pd.read_csv("data/ci_clustered.csv")
print("Data columns:", df.columns.tolist())
print("Number of rows:", len(df))
print("Unique clusters:")
for name, group in df.groupby(['final_cluster_nr', 'final_cluster_label']):
    print(f"Cluster number: {name[0]} - Label: {name[1]} - Size: {len(group)}")

for (cid, clabel), c_df in df.groupby(['final_cluster_nr', 'final_cluster_label']):
    print(f"\n--- Cluster {cid}: {clabel} (Count: {len(c_df)}, Pct: {len(c_df)/len(df)*100:.2f}%) ---")
    
    # Calculate averages
    print(f"Age: {c_df['age'].mean():.1f}")
    print(f"Female: {c_df['is_female'].mean():.2f}")
    print(f"Dependants: {c_df['dependants'].mean():.2f}")
    print(f"Total Spend: {c_df['total_spend'].mean():.2f}")
    print(f"Tenure: {c_df['customer_tenure'].mean():.1f}")
    print(f"Loyalty Card: {c_df['has_loyalty_card'].mean():.2f}")
    print(f"Number of complaints: {c_df['number_complaints'].mean():.2f}")
    print(f"Typical hour: {c_df['typical_hour'].mean():.1f}")
    print(f"Promotion pct: {c_df['percentage_of_products_bought_promotion'].mean():.2f}")
    print(f"Distinct stores: {c_df['distinct_stores_visited'].mean():.2f}")
    print(f"Distinct products: {c_df['lifetime_total_distinct_products'].mean():.2f}")
    
    # Shares
    shares = {col: c_df[col].mean() for col in df.columns if col.startswith('share_')}
    sorted_shares = sorted(shares.items(), key=lambda x: x[1], reverse=True)
    print("Top product shares:")
    for col, val in sorted_shares[:5]:
        print(f"  {col}: {val:.3f}")
        
    # Diets
    diets = c_df['dietary_preference'].value_counts(normalize=True) * 100
    print("Diet distribution:")
    for diet, pct in diets.items():
        print(f"  {diet}: {pct:.1f}%")
