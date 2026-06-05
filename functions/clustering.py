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


###### Analysis

def add_clusters(df_original, labels, cluster_col='cluster'):
    """
    Attach cluster labels to the original dataframe
    """
    return df_original.assign(**{cluster_col: labels})


def cluster_size_summary(clustered_df, cluster_col='cluster'):
    """
    Customer count and share per cluster
    """
    sizes = clustered_df[cluster_col].value_counts().sort_index()
    return pd.DataFrame({
        cluster_col: sizes.index,
        'n_customers': sizes.values,
        'customer_share': (sizes.values / len(clustered_df)).round(4)})


def profile_clusters(clustered_df, profile_cols, cluster_col='cluster'):
    """
    Mean and median of each feature per cluster
    """
    return clustered_df.groupby(cluster_col)[profile_cols].agg(['mean', 'median']).round(2)


def cluster_mean_profile(clustered_df, profile_cols, cluster_col='cluster'):
    """
    Cluster means joined with size stats in a flat table
    """
    profile = clustered_df.groupby(cluster_col)[profile_cols].mean().round(3)
    sizes = cluster_size_summary(clustered_df, cluster_col).set_index(cluster_col)
    return sizes.join(profile).reset_index()


def cluster_lift_profile(clustered_df, profile_cols, cluster_col='cluster'):
    """
    Ratio of each cluster mean to the overall mean (lift > 1 = above average)
    """
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean().replace(0, np.nan)
    return cluster_means.divide(overall_means, axis=1).round(3).replace([np.inf, -np.inf], np.nan)


def top_cluster_differences(clustered_df, profile_cols, cluster_col='cluster', top_n=6):
    """
    Top above/below-average features per cluster, ranked by z-score
    """
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean()
    overall_std = clustered_df[profile_cols].std().replace(0, np.nan)
    z_diffs = cluster_means.subtract(overall_means, axis=1).divide(overall_std, axis=1)

    rows = []
    for cluster_label, values in z_diffs.iterrows():
        values = values.dropna().sort_values()
        for feature, score in values.head(top_n).items():
            rows.append({cluster_col: cluster_label, 'direction': 'below_average', 'feature': feature, 'z': round(score, 3)})
        for feature, score in values.tail(top_n).sort_values(ascending=False).items():
            rows.append({cluster_col: cluster_label, 'direction': 'above_average', 'feature': feature, 'z': round(score, 3)})

    return pd.DataFrame(rows)


def analyze_cluster_patterns(df_original, labels, feature_cols):
    """
    Comprehensive analysis of the generated clusters.
    Prints cluster sizes, the most distinct features for each cluster, 
    and plots a heatmap of the cluster profiles.
    """
    from IPython.display import display
    
    # Add labels to original dataframe
    clustered_df = add_clusters(df_original, labels)
    
    print("\n" + "="*50)
    print("                 CLUSTER SIZES")
    print("="*50)
    sizes = cluster_size_summary(clustered_df)
    display(sizes)
    
    print("\n" + "="*50)
    print("        TOP DEFINING FEATURES PER CLUSTER")
    print("="*50)
    top_diffs = top_cluster_differences(clustered_df, feature_cols, top_n=4)
    display(top_diffs)
    
    print("\n" + "="*50)
    print("       CLUSTER HEATMAP (Z-Scores vs Global Mean)")
    print("="*50)
    plot_cluster_feature_heatmap(clustered_df, feature_cols)
    
    return clustered_df


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


def plot_pca_cluster_map(df_scaled, feature_cols, labels):
    """
    Scatter plot of clusters projected to 2 PCA dimensions
    """
    coords = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(df_scaled[feature_cols])
    plot_df = pd.DataFrame({'pca_1': coords[:, 0], 'pca_2': coords[:, 1], 'cluster': labels})

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x='pca_1', y='pca_2', hue='cluster', palette='tab10', s=18, alpha=0.7)
    plt.title('Customer segments — PCA')
    plt.tight_layout()
    plt.show()


def plot_umap_cluster_map(df_scaled, feature_cols, labels, n_neighbors=15, min_dist=0.1):
    """
    Scatter plot of clusters projected with UMAP
    """
    import umap
    coords = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, random_state=RANDOM_STATE).fit_transform(df_scaled[feature_cols])
    plot_df = pd.DataFrame({'umap_1': coords[:, 0], 'umap_2': coords[:, 1], 'cluster': labels})

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x='umap_1', y='umap_2', hue='cluster', palette='tab10', s=18, alpha=0.7)
    plt.title('Customer segments — UMAP')
    plt.tight_layout()
    plt.show()





# Export

#### Provavelmente nao vao ser necessarios

def export_customer_clusters(clustered_df, output_path='customer_clusters.csv'):
    """
    Export customer_id and cluster to CSV
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    output = clustered_df[['customer_id', 'cluster']]
    output.to_csv(output_path, index=False)
    return output


def export_cluster_profile(clustered_df, profile_cols, output_path='outputs/cluster_profile.csv'):
    """
    Export the flat cluster mean profile to CSV
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    output = cluster_mean_profile(clustered_df, profile_cols)
    output.to_csv(output_path, index=False)
    return output
