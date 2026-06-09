import os
import sys
import json
import pandas as pd
import numpy as np
import umap
from sklearn.preprocessing import RobustScaler

# Add project root to sys.path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FEATURE_COLS and scale_features directly from the project's preprocessing module
from functions.preprocessing import FEATURE_COLS, scale_features

print("Running real UMAP calculation importing from functions.preprocessing...")

# 1. Load the clustered dataset
df = pd.read_csv('data/ci_clustered.csv')
print(f"Loaded dataset: {len(df)} rows.")

# 2. Scale features using their exact scale_features implementation
df_scaled = scale_features(df.copy(), RobustScaler)
print("Features scaled using scale_features(df, RobustScaler) from functions.preprocessing.")

# 3. Fit UMAP on the full scaled feature space using the notebook's exact hyperparameters
print("Running UMAP dimensionality reduction on 32,571 points...")
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
coords = reducer.fit_transform(df_scaled[FEATURE_COLS])
print("UMAP coordinates generated.")

# 4. Attach UMAP dimensions and final cluster numbers
df_coords = pd.DataFrame({
    'umap_1': coords[:, 0],
    'umap_2': coords[:, 1],
    'cluster': df['final_cluster_nr']
})

# 5. Densely sample 5,000 total points proportionally to preserve the exact layout and density of the notebook's plot
# (a sparse 700 points looks empty; 5,000 points maintains the beautiful 'islands' topology while remaining fast in Plotly)
total_sample_size = 5000
sampled_groups = []

# Get proportions of each cluster in the full dataset
cluster_counts = df_coords['cluster'].value_counts()
total_rows = len(df_coords)

for cluster_nr in sorted(df_coords['cluster'].unique()):
    cluster_df = df_coords[df_coords['cluster'] == cluster_nr]
    # Calculate proportional sample size for this cluster
    prop = len(cluster_df) / total_rows
    cluster_sample_size = int(round(prop * total_sample_size))
    
    sampled_cluster = cluster_df.sample(n=min(cluster_sample_size, len(cluster_df)), random_state=42)
    sampled_groups.append({
        'cluster': int(cluster_nr),
        'x': [round(val, 4) for val in sampled_cluster['umap_1'].tolist()],
        'y': [round(val, 4) for val in sampled_cluster['umap_2'].tolist()]
    })
    print(f"Sampled {len(sampled_cluster)} points for cluster {cluster_nr} ({cluster_nr}) - proportional size.")

# 6. Save UMAP coordinates to JSON
output_path = 'dashboard/src/data/umap_sampled.json'
with open(output_path, 'w') as f:
    json.dump(sampled_groups, f, indent=2)

print(f"Real UMAP coordinates successfully saved to {output_path}!")
