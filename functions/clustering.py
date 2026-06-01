import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans, MeanShift, estimate_bandwidth
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score)
from sklearn.manifold import TSNE


RANDOM_STATE = 42


def get_model_matrix(df, feature_cols):
    """Return only the scaled numeric features used by clustering models."""
    return df[feature_cols].copy()


def calculate_cluster_metrics(X, labels):
    """Calculate clustering metrics when the solution has at least 2 clusters."""
    labels = np.asarray(labels)
    unique_labels = set(labels)

    # DBSCAN may create noise as -1. Keep it in size counts, but ignore all-noise cases.
    valid_clusters = unique_labels.difference({-1})
    if len(valid_clusters) < 2:
        return {
            'n_clusters': len(valid_clusters),
            'silhouette': np.nan,
            'davies_bouldin': np.nan,
            'calinski_harabasz': np.nan,
        }

    return {
        'n_clusters': len(valid_clusters),
        'silhouette': silhouette_score(X, labels)
    }


def compare_clustering_models(df_scaled, feature_cols, k_range=range(3, 11)):
    """Compare K-Means and hierarchical clustering across several cluster counts."""
    X = get_model_matrix(df_scaled, feature_cols)
    results = []

    for k in k_range:
        models = {
            'kmeans': KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init='auto'),
            'hierarchical_ward': AgglomerativeClustering(n_clusters=k, linkage='ward'),
        }

        for model_name, model in models.items():
            labels = model.fit_predict(X)
            metrics = calculate_cluster_metrics(X, labels)
            cluster_sizes = pd.Series(labels).value_counts()

            results.append({
                'model': model_name,
                'k': k,
                **metrics,
                'min_cluster_size': cluster_sizes.min(),
                'max_cluster_size': cluster_sizes.max(),
                'smallest_cluster_share': cluster_sizes.min() / len(labels),
                'largest_cluster_share': cluster_sizes.max() / len(labels),
            })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'davies_bouldin'], ascending=[False, True])
        .reset_index(drop=True)
    )


def compare_dbscan(df_scaled, feature_cols, eps_values=(0.8, 1.0, 1.2, 1.5), min_samples_values=(10, 25, 50)):
    """Compare DBSCAN settings, mostly to understand density groups and outliers."""
    X = get_model_matrix(df_scaled, feature_cols)
    results = []

    for eps in eps_values:
        for min_samples in min_samples_values:
            labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
            metrics = calculate_cluster_metrics(X, labels)
            noise_share = (labels == -1).mean()
            cluster_sizes = pd.Series(labels[labels != -1]).value_counts()

            results.append({
                'model': 'dbscan',
                'eps': eps,
                'min_samples': min_samples,
                **metrics,
                'noise_share': noise_share,
                'min_cluster_size': cluster_sizes.min() if len(cluster_sizes) else 0,
                'max_cluster_size': cluster_sizes.max() if len(cluster_sizes) else 0,
            })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'noise_share'], ascending=[False, True])
        .reset_index(drop=True)
    )


def check_dbscan_outliers(df_scaled, feature_cols, eps_values=(0.8, 1.0, 1.2, 1.5), min_samples=25):
    """Use DBSCAN as the professor suggested: mainly to inspect noise/outliers."""
    return compare_dbscan(
        df_scaled,
        feature_cols,
        eps_values=eps_values,
        min_samples_values=(min_samples,),
    )


def compare_mean_shift(df_scaled, feature_cols, quantiles=(0.1, 0.2, 0.3), sample_size=3000):
    """Compare Mean Shift bandwidths estimated from different quantiles."""
    X = get_model_matrix(df_scaled, feature_cols)
    results = []

    for quantile in quantiles:
        bandwidth = estimate_bandwidth(
            X,
            quantile=quantile,
            n_samples=min(sample_size, len(X)),
            random_state=RANDOM_STATE,
        )

        if bandwidth <= 0:
            continue

        labels = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit_predict(X)
        metrics = calculate_cluster_metrics(X, labels)
        cluster_sizes = pd.Series(labels).value_counts()

        results.append({
            'model': 'mean_shift',
            'quantile': quantile,
            'bandwidth': bandwidth,
            **metrics,
            'min_cluster_size': cluster_sizes.min(),
            'max_cluster_size': cluster_sizes.max(),
            'smallest_cluster_share': cluster_sizes.min() / len(labels),
            'largest_cluster_share': cluster_sizes.max() / len(labels),
        })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'davies_bouldin'], ascending=[False, True])
        .reset_index(drop=True)
    )


def fit_final_kmeans(df_scaled, feature_cols, n_clusters):
    """Fit the final K-Means segmentation and return labels plus fitted model."""
    X = get_model_matrix(df_scaled, feature_cols)
    model = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init='auto')
    labels = model.fit_predict(X)
    return labels, model


def fit_final_hierarchical(df_scaled, feature_cols, n_clusters, linkage='ward'):
    """Fit the final hierarchical clustering segmentation."""
    X = get_model_matrix(df_scaled, feature_cols)
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    labels = model.fit_predict(X)
    return labels, model


def fit_final_dbscan(df_scaled, feature_cols, eps, min_samples=25):
    """Fit DBSCAN if the density-based result is meaningful enough to use."""
    X = get_model_matrix(df_scaled, feature_cols)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    return labels, model


def fit_final_mean_shift(df_scaled, feature_cols, bandwidth=None, quantile=0.2, sample_size=3000):
    """Fit Mean Shift using either a chosen bandwidth or an estimated one."""
    X = get_model_matrix(df_scaled, feature_cols)
    if bandwidth is None:
        bandwidth = estimate_bandwidth(
            X,
            quantile=quantile,
            n_samples=min(sample_size, len(X)),
            random_state=RANDOM_STATE,
        )
    model = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    labels = model.fit_predict(X)
    return labels, model


def add_clusters(df_original, labels, cluster_col='cluster'):
    """Attach cluster labels to the original customer-level dataframe."""
    clustered = df_original.copy()
    clustered[cluster_col] = labels
    return clustered


def cluster_size_summary(clustered_df, cluster_col='cluster'):
    """Summarize how many customers are assigned to each segment."""
    sizes = clustered_df[cluster_col].value_counts().sort_index()
    return pd.DataFrame({
        cluster_col: sizes.index,
        'n_customers': sizes.values,
        'customer_share': sizes.values / len(clustered_df),
    })


def profile_clusters(clustered_df, profile_cols, cluster_col='cluster'):
    """Create an interpretable segment profile using the unscaled original values."""
    return clustered_df.groupby(cluster_col)[profile_cols].agg(['mean', 'median']).round(2)


def plot_metric_comparison(results):
    """Plot model quality metrics to support the cluster-count decision."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    sns.lineplot(data=results, x='k', y='silhouette', hue='model', marker='o', ax=axes[0])
    axes[0].set_title('Silhouette score')

    sns.lineplot(data=results, x='k', y='davies_bouldin', hue='model', marker='o', ax=axes[1])
    axes[1].set_title('Davies-Bouldin score')

    sns.lineplot(data=results, x='k', y='calinski_harabasz', hue='model', marker='o', ax=axes[2])
    axes[2].set_title('Calinski-Harabasz score')

    plt.tight_layout()
    plt.show()


def plot_pca_cluster_map(df_scaled, feature_cols, labels):
    """Show clusters in two PCA dimensions for a quick visual sanity check."""
    X = get_model_matrix(df_scaled, feature_cols)
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    coordinates = pca.fit_transform(X)

    plot_df = pd.DataFrame({
        'pca_1': coordinates[:, 0],
        'pca_2': coordinates[:, 1],
        'cluster': labels,
    })

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=plot_df,
        x='pca_1',
        y='pca_2',
        hue='cluster',
        palette='tab10',
        s=18,
        alpha=0.7,
    )
    plt.title('Customer segments projected with PCA')
    plt.tight_layout()
    plt.show()


def plot_tsne_cluster_map(df_scaled, feature_cols, labels, perplexity=30):
    """Show clusters with t-SNE for non-linear visual inspection."""
    X = get_model_matrix(df_scaled, feature_cols)
    coordinates = TSNE(
        n_components=2,
        perplexity=perplexity,
        random_state=RANDOM_STATE,
        init='pca',
        learning_rate='auto',
    ).fit_transform(X)

    plot_df = pd.DataFrame({
        'tsne_1': coordinates[:, 0],
        'tsne_2': coordinates[:, 1],
        'cluster': labels,
    })

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=plot_df,
        x='tsne_1',
        y='tsne_2',
        hue='cluster',
        palette='tab10',
        s=18,
        alpha=0.7,
    )
    plt.title('Customer segments projected with t-SNE')
    plt.tight_layout()
    plt.show()


def plot_umap_cluster_map(df_scaled, feature_cols, labels, n_neighbors=15, min_dist=0.1):
    """Show clusters with UMAP, useful for visual segment separation."""
    import umap

    X = get_model_matrix(df_scaled, feature_cols)
    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=RANDOM_STATE,
    )
    coordinates = reducer.fit_transform(X)

    plot_df = pd.DataFrame({
        'umap_1': coordinates[:, 0],
        'umap_2': coordinates[:, 1],
        'cluster': labels,
    })

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=plot_df,
        x='umap_1',
        y='umap_2',
        hue='cluster',
        palette='tab10',
        s=18,
        alpha=0.7,
    )
    plt.title('Customer segments projected with UMAP')
    plt.tight_layout()
    plt.show()


def plot_cluster_map(df_scaled, feature_cols, labels):
    """Backward-compatible alias for the PCA cluster map."""
    plot_pca_cluster_map(df_scaled, feature_cols, labels)


def export_customer_clusters(clustered_df, output_path='customer_clusters.csv'):
    """Export the required final file: customer_id and proposed cluster."""
    output = clustered_df[['customer_id', 'cluster']].copy()

    if output['customer_id'].duplicated().any():
        raise ValueError('customer_id appears more than once in the cluster output.')

    output.to_csv(output_path, index=False)
    return output
