import pandas as pd
import sys

try:
    persons = pd.read_csv("data/persons_clustered.csv")
    ci = pd.read_csv("data/ci_clustered.csv")
    
    print("persons_clustered.csv shapes:", persons.shape)
    print("ci_clustered.csv shapes:", ci.shape)
    
    # Check if 'customer_id' exists in both
    if 'customer_id' in persons.columns and 'customer_id' in ci.columns:
        # Join by customer_id
        merged = pd.merge(persons[['customer_id', 'Final_Cluster']], ci[['customer_id', 'final_cluster_label']], on='customer_id', how='inner')
        print("\nMapping of Original 'Final_Cluster' vs 'final_cluster_label' for the SAME customer_id:")
        print(pd.crosstab(merged['Final_Cluster'], merged['final_cluster_label']))
        
    else:
        print("Columns missing")
except Exception as e:
    print("Error:", e)
