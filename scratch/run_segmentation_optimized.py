import os
import sys
import pandas as pd
from sklearn.preprocessing import RobustScaler

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.preprocessing import FEATURE_COLS, scale_features
from functions.clustering import fit_final_kmeans

print("Running optimized 9-cluster solution generation...")

# 1. Load data
clean_data = pd.read_csv('data/ci_clustering.csv')
print(f"Loaded {len(clean_data)} rows of raw customer data.")

# 2. Separate vegans (vegetarian dietary preference)
vegans = clean_data[clean_data['dietary_preference'] == 'vegetarian'].copy()
clean_data = clean_data[clean_data['dietary_preference'] != 'vegetarian'].copy().reset_index(drop=True)
print(f"Split data: {len(clean_data)} non-vegans, {len(vegans)} vegans.")

# 3. Preprocess and scale non-vegans using RobustScaler
clean_rb = scale_features(clean_data.copy(), RobustScaler)
print("Scaled non-vegan features using RobustScaler.")

# 4. Fit K-Means with 8 clusters on non-vegans
print("Fitting K-Means model (k=8)...")
kmeans_labels_rb, kmeans_model_rb = fit_final_kmeans(clean_rb, FEATURE_COLS, n_clusters=8)

# Add cluster labels to non-vegans
clean_data['final_cluster_nr'] = kmeans_labels_rb

# 5. Set vegans cluster number to 8
vegans['final_cluster_nr'] = 8

# 6. Combine vegans and non-vegans back
clean_data = pd.concat([clean_data, vegans], axis=0).reset_index(drop=True)
print(f"Merged combined data size: {len(clean_data)} rows.")

# 7. Map final cluster numbers to labels
clusters_mapping = {
    0: 'Bargain hunters',
    1: 'Tech enthusiasts',
    2: 'Big families (big spenders)',
    3: 'Clean and healthy',
    4: 'Average customer',
    5: 'Gamers',
    6: 'Loyal big spenders',
    7: 'Karens',
    8: 'Vegans'
}

clean_data['final_cluster_label'] = clean_data['final_cluster_nr'].map(clusters_mapping)

# 8. Check value counts
print("\nCluster Distribution:")
print(clean_data['final_cluster_label'].value_counts())
print(clean_data['final_cluster_nr'].value_counts())

# 9. Save to data/ci_clustered.csv
output_path = 'data/ci_clustered.csv'
clean_data.to_csv(output_path, index=False)
print(f"\nSaved final 9-cluster dataset successfully to {output_path}!")
