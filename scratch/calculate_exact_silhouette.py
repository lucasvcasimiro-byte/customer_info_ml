import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from functions.preprocessing import FEATURE_COLS

# Load the clustering dataset
df = pd.read_csv("data/ci_clustering.csv")

X_raw = df[FEATURE_COLS]

scalers = {
    'StandardScaler': StandardScaler,
    'RobustScaler': RobustScaler,
    'MinMaxScaler': MinMaxScaler
}

k_values = [5, 6, 7]
SAMPLE_SIZE = 5000
RANDOM_STATE = 42

print("Running calculations...")

results = {}

for name, scaler_cls in scalers.items():
    scaler = scaler_cls()
    X_scaled = scaler.fit_transform(X_raw)
    X_scaled_df = pd.DataFrame(X_scaled, columns=FEATURE_COLS)
    
    # Sample for silhouette score (standard behavior in their functions/clustering.py)
    X_sample = X_scaled_df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=RANDOM_STATE)
    
    for k in k_values:
        # KMeans inertia on full data
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        kmeans.fit(X_scaled_df)
        inertia = kmeans.inertia_
        
        # Silhouette score of K-Means (sampled)
        kmeans_sample = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels_kmeans = kmeans_sample.fit_predict(X_sample)
        silhouette_kmeans = silhouette_score(X_sample, labels_kmeans)
        
        # Hierarchical Clustering (sampled)
        ward = AgglomerativeClustering(n_clusters=k, linkage='ward')
        labels_ward = ward.fit_predict(X_sample)
        silhouette_ward = silhouette_score(X_sample, labels_ward)
        
        print(f"{name}__k={k}:")
        print(f"  KMeans Inertia: {inertia:.1f}")
        print(f"  KMeans Silhouette: {silhouette_kmeans:.4f}")
        print(f"  Ward Silhouette: {silhouette_ward:.4f}")
