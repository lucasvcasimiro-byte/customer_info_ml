import pandas as pd

print("Loading data...")
info = pd.read_csv("data/customer_info.csv")
clustered = pd.read_csv("data/ci_clustered.csv")

# Merge by customer_id
merged = pd.merge(info[['customer_id', 'number_complaints']], 
                  clustered[['customer_id', 'number_complaints']], 
                  on='customer_id', suffixes=('_info', '_clustered'))

# Check if number_complaints matches for the same customer_id
mismatches = merged[merged['number_complaints_info'] != merged['number_complaints_clustered']]

print(f"Total rows merged: {len(merged)}")
print(f"Number of mismatches in 'number_complaints': {len(mismatches)}")

if len(mismatches) > 0:
    print("\nFirst 5 mismatches:")
    print(mismatches.head())
    
    # Try joining by index instead to see if that matches
    merged_by_index = pd.merge(info[['customer_id', 'number_complaints']], 
                               clustered[['customer_id', 'number_complaints']], 
                               left_index=True, right_index=True, suffixes=('_info', '_clustered'))
    
    index_mismatches = merged_by_index[merged_by_index['number_complaints_info'] != merged_by_index['number_complaints_clustered']]
    print(f"\nNumber of mismatches if we join by row index instead: {len(index_mismatches)}")
