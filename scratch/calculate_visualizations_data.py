import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_samples, silhouette_score
import umap
from sklearn.feature_selection import f_classif
from functions.preprocessing import FEATURE_COLS

# Load data
df = pd.read_csv("data/ci_clustered.csv")
print("Total records loaded:", len(df))

# Features and labels
X_raw = df[FEATURE_COLS]
labels = df['final_cluster_nr']
label_names = df['final_cluster_label']

# Scale features using RobustScaler (which was chosen for final clustering)
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_raw)

# 1. Calculate UMAP 2D Projection
print("Fitting UMAP...")
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
embedding = reducer.fit_transform(X_scaled)

df['umap_x'] = embedding[:, 0]
df['umap_y'] = embedding[:, 1]

# Sample 50 points per cluster to keep the frontend payload small and performant
sampled_points = []
for cid in sorted(labels.unique()):
    c_df = df[df['final_cluster_nr'] == cid]
    # Sample 50 rows
    sampled_c = c_df.sample(n=min(50, len(c_df)), random_state=42)
    sampled_points.append({
        'cluster': int(cid),
        'name': str(sampled_c['final_cluster_label'].iloc[0]),
        'x': sampled_c['umap_x'].tolist(),
        'y': sampled_c['umap_y'].tolist()
    })

# 2. Calculate Silhouette per Cluster
# Since silhouette_samples on 32k rows takes memory/time, let's sample 5000 rows
print("Calculating Silhouette per cluster...")
sample_idx = df.sample(n=5000, random_state=42).index
X_sample = X_scaled[df.index.isin(sample_idx)]
labels_sample = labels[df.index.isin(sample_idx)]
label_names_sample = label_names[df.index.isin(sample_idx)]

sil_vals = silhouette_samples(X_sample, labels_sample)
df_sil = pd.DataFrame({'cluster': labels_sample, 'label': label_names_sample, 'sil': sil_vals})

sil_per_cluster = {}
for name, group in df_sil.groupby('cluster'):
    label = group['label'].iloc[0]
    sil_per_cluster[int(name)] = {
        'label': label,
        'avg_sil': float(group['sil'].mean())
    }

print("Avg Silhouette per cluster:", sil_per_cluster)

# 3. Calculate Feature Importance via ANOVA F-value
print("Calculating feature importance...")
f_vals, p_vals = f_classif(X_scaled, labels)
# Normalize F-values to sum to 100% to represent relative importance
total_f = sum(f_vals)
importance = (f_vals / total_f) * 100

feat_imp = []
for feat, imp in zip(FEATURE_COLS, importance):
    # Format name for display
    name = feat.replace('share_', '').replace('lifetime_spend_', '').replace('_', ' ').title()
    feat_imp.append({'feature': name, 'raw_feature': feat, 'importance': round(imp, 2)})
    
# Sort by importance
feat_imp = sorted(feat_imp, key=lambda x: x['importance'], reverse=True)
print("Top features by importance:")
for item in feat_imp[:10]:
    print(f"  {item['feature']}: {item['importance']:.2f}%")

# Save outputs to JSON so we can easily paste them
output = {
    'pcaData': sampled_points,
    'silhouettePerCluster': sil_per_cluster,
    'featureImportance': feat_imp
}

with open("scratch/viz_data.json", "w") as f:
    json.dump(output, f, indent=2)
print("Saved viz data to scratch/viz_data.json!")
