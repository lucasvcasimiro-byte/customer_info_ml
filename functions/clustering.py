import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


RANDOM_STATE = 42
SAMPLE_SIZE = 5000

##### Model comparisons

def compare_clustering_models(df_scaled, feature_cols, k_range=range(3, 11)):
    """
    Compare K-Means and ward hierarchical clustering across k values (silhouette score)
    """
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)
    results = []

    for k in k_range:
        for name, model in [
            ('kmeans', KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)),
            ('hierarchical_ward', AgglomerativeClustering(n_clusters=k, linkage='ward'))]:
            labels = model.fit_predict(X)

            results.append({'model': name, 'k': k, 'silhouette': silhouette_score(X, labels)})

    return pd.DataFrame(results).sort_values('silhouette', ascending=False).reset_index(drop=True)


def compare_kmeans_inertia(df_scaled, feature_cols, k_range=range(1, 11)):
    """
    Compute K-Means inertia for the elbow method and plots it 
    """
    X = df_scaled[feature_cols]
    inertia_df = pd.DataFrame([
        {'k': k, 'inertia': KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10).fit(X).inertia_}
        for k in k_range])

    # Plot the elbow curve
    plt.figure(figsize=(8, 5))
    plt.plot(inertia_df['k'], inertia_df['inertia'], marker='o', linewidth=2, color='steelblue')
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.xticks(inertia_df['k'])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return inertia_df


######## Final fitting

def fit_final_kmeans(df_scaled, feature_cols, n_clusters):
    """
    Fit the final K-Means model on the full dataset
    """
    X = df_scaled[feature_cols]
    model = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    return model.fit_predict(X), model


def fit_final_hierarchical(df_scaled, feature_cols, n_clusters, linkage_method='ward'):
    """
    Fit the final Hierarchical Clustering model on the full dataset
    """
    X = df_scaled[feature_cols]
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method, metric='euclidean')
    return model.fit_predict(X), model


###### Analysis

def add_clusters(df_original, labels, cluster_col='cluster'):
    """
    Attach cluster labels to the original dataframe
    """
    return df_original.assign(**{cluster_col: labels})

def calculate_group_means(df, cluster_col):
    """
    Calculates the mean of all numeric features grouped by a specific cluster column
    """
    return df.groupby(cluster_col).mean(numeric_only=True).T


####### Plots

def plot_r2_hc(df_scaled, feature_cols, max_nclus=10, min_nclus=2):
    """
    Plots the R2 statistic for different hierarchical clustering linkage methods,
    proving the superiority of 'ward' at explaining variance.
    """
    # Sample data to avoid MemoryError in AgglomerativeClustering
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)
    
    def get_ss(df):
        return np.sum(df.var() * (df.count() - 1))

    sst = get_ss(X)
    hc_methods = ["ward", "complete", "average", "single"]
    
    results = {method: [] for method in hc_methods}
    k_range = list(range(min_nclus, max_nclus + 1))
    
    for method in hc_methods:
        for k in k_range:
            cluster = AgglomerativeClustering(n_clusters=k, metric="euclidean", linkage=method)
            labels = cluster.fit_predict(X)
            
            X_concat = pd.concat((X, pd.Series(labels, name='labels', index=X.index)), axis=1)
            ssw_labels = X_concat.groupby('labels').apply(get_ss)
            ssb = sst - np.sum(ssw_labels)
            results[method].append(ssb / sst)

    r2_df = pd.DataFrame(results, index=k_range)
    
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=r2_df, linewidth=2.5, markers=["o"]*4)
    plt.title("R² Metric by Hierarchical Linkage Method", fontsize=16)
    plt.xlabel("Number of Clusters (k)", fontsize=12)
    plt.ylabel("R² (Explained Variance)", fontsize=12)
    plt.xticks(k_range)
    plt.gca().invert_xaxis()
    plt.grid(True, alpha=0.3)
    plt.legend(title="Linkage Methods")
    plt.tight_layout()
    plt.show()

def plot_dendrogram(df_scaled, feature_cols, linkage_method='ward', truncate_p=5):
    """
    Plots a hierarchical clustering dendrogram using scipy.
    Samples the data and truncates the plot to only show the top p levels.
    """
    from scipy.cluster import hierarchy
    
    # Sample data 
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)
    
    # Calculate the linkage matrix
    Z = hierarchy.linkage(X, method=linkage_method, metric='euclidean')
    
    plt.figure(figsize=(10, 6))
    hierarchy.dendrogram(
        Z,
        truncate_mode='level',
        p=truncate_p,
        show_leaf_counts=True,
        leaf_rotation=90.,
        leaf_font_size=10.,
        show_contracted=True
    )
    plt.title(f'Hierarchical Clustering Dendrogram (Truncated top {truncate_p} levels)')
    plt.xlabel('Cluster size (or individual index)')
    plt.ylabel('Distance')
    plt.tight_layout()
    plt.show()


def plot_metric_comparison(results):
    """
    Plot silhouette score vs k per model
    """
    plt.figure(figsize=(7, 4))
    sns.lineplot(data=results, x='k', y='silhouette', hue='model', marker='o')
    plt.title('Silhouette score by number of clusters')
    plt.tight_layout()
    plt.show()


def plot_cluster_feature_heatmap(clustered_df, profile_cols, cluster_col='cluster'):
    """
    Heatmap of standardized cluster means (z-scores vs overall mean)
    """
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean()
    overall_std = clustered_df[profile_cols].std().replace(0, np.nan)
    heatmap_data = cluster_means.subtract(overall_means, axis=1).divide(overall_std, axis=1)

    plt.figure(figsize=(14, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', center=0, linewidths=0.3, linecolor='white',
                cbar_kws={'label': 'Std deviations from overall mean'})
    plt.title('Cluster profile heatmap')
    plt.tight_layout()
    plt.show()


def plot_umap_cluster_map(df_scaled, feature_cols, labels, n_neighbors=15, min_dist=0.1):
    """
    Scatter plot of clusters projected with UMAP
    """
    import umap
    # Using pure Unsupervised UMAP to show the true mathematical topology of the data.
    coords = umap.UMAP(
        n_neighbors=n_neighbors, 
        min_dist=min_dist, 
        random_state=RANDOM_STATE
    ).fit_transform(df_scaled[feature_cols])
    plot_df = pd.DataFrame({'umap_1': coords[:, 0], 'umap_2': coords[:, 1], 'cluster': labels})

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x='umap_1', y='umap_2', hue='cluster', palette='tab10', s=18, alpha=0.7)
    plt.title('Customer segments — UMAP')
    plt.tight_layout()
    plt.show()


def plot_cluster_geography(df, labels, point_size=12, alpha=0.7, cols=3):
    """
    Plots the geographic distribution of customers as a grid of maps (one per cluster).
    Input df has to be the original, not the one used for clustering.
    """
    import math
    import geopandas as gpd
    import contextily as ctx
    from shapely.geometry import Point
    from pyproj import Transformer

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("Error: DataFrame must contain 'latitude' and 'longitude' columns.")
        return

    df = df.copy()
    df['cluster'] = labels

    # Build GeoDataFrame
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    gdf_merc = gdf.to_crs(epsg=3857)

    cluster_ids = sorted(df['cluster'].unique())
    n_clusters = len(cluster_ids)
    palette = sns.color_palette('tab10', n_clusters)
    color_map = {c: palette[i] for i, c in enumerate(cluster_ids)}

    rows = math.ceil(n_clusters / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    
    # Flatten axes for easy iteration
    if isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = [axes]

    # Pre-calculate bounds for all subplots to keep maps consistent
    x_min, y_min, x_max, y_max = gdf_merc.total_bounds
    x_pad = (x_max - x_min) * 0.15
    y_pad = (y_max - y_min) * 0.15
    xlim = (x_min - x_pad, x_max + x_pad)
    ylim = (y_min - y_pad, y_max + y_pad)

    # Pre-calculate ticks (only few ticks for small maps)
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    
    for i in range(len(axes)):
        ax = axes[i]
        
        # If we have more subplots than clusters, hide the extra ones
        if i >= n_clusters:
            ax.set_visible(False)
            continue
            
        cid = cluster_ids[i]
        color = color_map[cid]

        # 2. Plot highlight (this cluster's points)
        sub = gdf_merc[gdf_merc['cluster'] == cid]
        sub.plot(
            ax=ax, color=color, markersize=point_size, alpha=alpha, 
            linewidths=0.2, edgecolor='white'
        )
        
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title(f"Cluster {cid} (n={len(sub)})", fontweight='bold', color=color)
        
        # 3. Add basemap
        try:
            ctx.add_basemap(
                ax, crs=gdf_merc.crs.to_string(),
                source=ctx.providers.CartoDB.Positron,
                zoom="auto", attribution_size=4
            )
        except Exception:
            pass

        # 4. Format axes
        ax.tick_params(length=3, color="#AAAAAA", labelsize=7)
        ax.grid(True, alpha=0.15)
        
        # Convert tick labels to lat/lon for the first col and last row
        if i % cols == 0:
            ax.set_ylabel("Latitude", fontsize=8)
        else:
            ax.set_yticklabels([])
            
        if i >= len(axes) - cols:
            ax.set_xlabel("Longitude", fontsize=8)
        else:
            ax.set_xticklabels([])

    fig.suptitle("Geographic Distribution by Cluster", fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    plt.show()
