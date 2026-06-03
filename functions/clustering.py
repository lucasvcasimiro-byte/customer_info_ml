import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


RANDOM_STATE = 42
SAMPLE_SIZE = 5000


# Helper for DBScan

#### UNDERSTAND BETTER

def _silhouette(X, labels):
    """
    Silhouette score, ignoring DBSCAN noise points (-1)
    """
    labels = np.asarray(labels)
    mask = labels != -1
    X_clean = X.loc[mask] if isinstance(X, pd.DataFrame) else X[mask]
    labels_clean = labels[mask]
    if len(set(labels_clean)) < 2:
        return np.nan
    return silhouette_score(X_clean, labels_clean)


##### Model comparisons

def compare_clustering_models(df_scaled, feature_cols, k_range=range(3, 11)):
    """
    Compare K-Means and Ward hierarchical clustering across k values
    """
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)
    results = []

    for k in k_range:
        for name, model in [
            ('kmeans', KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)),
            ('hierarchical_ward', AgglomerativeClustering(n_clusters=k, linkage='ward'))]:
            labels = model.fit_predict(X)

            results.append({'model': name, 'k': k, 'silhouette': _silhouette(X, labels)})

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
    plt.title('Elbow Method – K-Means Inertia')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia (Within-cluster SSE)')
    plt.xticks(inertia_df['k'])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return inertia_df


def compare_kmeans_stability(df_scaled, feature_cols, k_range=range(3, 11), seeds=range(10)):
    """
    Check K-Means silhouette stability across random seeds
    """
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)

    results = [
        {'k': k, 'silhouette': _silhouette(X, KMeans(n_clusters=k, random_state=s, n_init=10).fit_predict(X))}
        for k in k_range for s in seeds
    ]
    return (
        pd.DataFrame(results)
        .groupby('k')['silhouette']
        .agg(['mean', 'std'])
        .rename(columns={'mean': 'silhouette_mean', 'std': 'silhouette_std'})
        .sort_values('silhouette_mean', ascending=False)
        .reset_index()
    )


def compare_dbscan(df_scaled, feature_cols, eps_values=(0.8, 1.0, 1.2, 1.5), min_samples_values=(10, 25, 50)):
    """
    Grid-search DBSCAN over eps and min_samples combinations
    """
    X = df_scaled[feature_cols].sample(n=min(SAMPLE_SIZE, len(df_scaled)), random_state=RANDOM_STATE)
    results = []

    for eps in eps_values:
        for min_samples in min_samples_values:
            labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
            results.append({
                'eps': eps,
                'min_samples': min_samples,
                'n_clusters': len(set(labels) - {-1}),
                'noise_share': round((labels == -1).mean(), 3),
                'silhouette': _silhouette(X, labels),
            })

    return pd.DataFrame(results).sort_values('silhouette', ascending=False).reset_index(drop=True)


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
        'customer_share': (sizes.values / len(clustered_df)).round(4),
    })


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


####### Plots

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
