import pandas as pd
import os

filepath = 'data/ci_clustered.csv'
if os.path.exists(filepath):
    df = pd.read_csv(filepath)
    print("Columns in ci_clustered.csv:", df.columns.tolist())
    print("\nValue counts of final_cluster_label:")
    if 'final_cluster_label' in df.columns:
        print(df['final_cluster_label'].value_counts())
    else:
        print("final_cluster_label column not found!")
    
    print("\nValue counts of final_cluster_nr:")
    if 'final_cluster_nr' in df.columns:
        print(df['final_cluster_nr'].value_counts())
    else:
        print("final_cluster_nr column not found!")
        
    print("\nIs vegetarian mapping aligned? (Vegans should be cluster 8):")
    if 'dietary_preference' in df.columns and 'final_cluster_nr' in df.columns:
        print(df.groupby('dietary_preference')['final_cluster_nr'].value_counts())
else:
    print(f"File {filepath} does not exist!")
