import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from functions.preprocessing import FEATURE_COLS

df = pd.read_csv("data/ci_clustering.csv")
X_scaled = RobustScaler().fit_transform(df[FEATURE_COLS])
X_scaled_df = pd.DataFrame(X_scaled, columns=FEATURE_COLS)
X_sample = X_scaled_df.sample(n=5000, random_state=42)

for k in range(3, 11):
    # KMeans
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    lbls_km = km.fit_predict(X_sample)
    sil_km = silhouette_score(X_sample, lbls_km)
    
    # Ward
    wd = AgglomerativeClustering(n_clusters=k, linkage='ward')
    lbls_wd = wd.fit_predict(X_sample)
    sil_wd = silhouette_score(X_sample, lbls_wd)
    
    print(f"k={k}: KMeans={sil_km:.4f}, Ward={sil_wd:.4f}")
