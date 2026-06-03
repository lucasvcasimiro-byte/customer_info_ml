import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans, MeanShift, estimate_bandwidth
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE


RANDOM_STATE = 42
DEFAULT_METRIC_SAMPLE_SIZE = 5000


def get_model_matrix(df, feature_cols):
    """
    Return only the scaled numeric features used by clustering models
    """
    # 
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f'Missing clustering features: {missing_cols}')

    X = df[feature_cols].copy()
    non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    if non_numeric_cols:
        raise TypeError(f'Clustering features must be numeric: {non_numeric_cols}')

    missing_values = X.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        raise ValueError(f'Clustering matrix still has missing values:\n{missing_values}')

    return X


def _metric_data_without_noise(X, labels):
    """Return data used for validation metrics, excluding DBSCAN noise labels."""
    labels = np.asarray(labels)
    non_noise_mask = labels != -1

    if -1 in labels:
        X_eval = X.loc[non_noise_mask] if isinstance(X, pd.DataFrame) else X[non_noise_mask]
        labels_eval = labels[non_noise_mask]
        return X_eval, labels_eval

    return X, labels


def _sample_metric_data(X, labels, sample_size=DEFAULT_METRIC_SAMPLE_SIZE, random_state=RANDOM_STATE):
    """Sample rows for validation metrics that are expensive on large datasets."""
    labels = np.asarray(labels)

    if sample_size is None or len(labels) <= sample_size:
        return X, labels

    rng = np.random.default_rng(random_state)
    sample_index = np.sort(rng.choice(len(labels), size=sample_size, replace=False))
    X_sample = X.iloc[sample_index] if isinstance(X, pd.DataFrame) else X[sample_index]
    return X_sample, labels[sample_index]


def _sample_model_data(X, sample_size=DEFAULT_METRIC_SAMPLE_SIZE, random_state=RANDOM_STATE):
    """Sample the model matrix for slower exploratory algorithms."""
    if sample_size is None or len(X) <= sample_size:
        return X
    return X.sample(n=sample_size, random_state=random_state)


def calculate_cluster_metrics(
    X,
    labels,
    sample_size=DEFAULT_METRIC_SAMPLE_SIZE,
    random_state=RANDOM_STATE,
):
    """
    Calculate clustering metrics when the solution has at least 2 real clusters.

    DBSCAN noise points labelled -1 are excluded from validation scores so that
    the noise flag is not treated as an ordinary customer segment.
    """
    labels = np.asarray(labels)
    X_eval, labels_eval = _metric_data_without_noise(X, labels)
    X_eval, labels_eval = _sample_metric_data(
        X_eval,
        labels_eval,
        sample_size=sample_size,
        random_state=random_state,
    )
    valid_clusters = set(labels_eval)

    if len(valid_clusters) < 2 or len(labels_eval) <= len(valid_clusters):
        return {
            'n_clusters': len(valid_clusters),
            'n_metric_rows': len(labels_eval),
            'silhouette': np.nan,
        }

    return {
        'n_clusters': len(valid_clusters),
        'n_metric_rows': len(labels_eval),
        'silhouette': silhouette_score(X_eval, labels_eval),
    }


def _cluster_size_stats(labels):
    """Return size diagnostics used to avoid tiny or dominant cluster choices."""
    labels = np.asarray(labels)
    sizes = pd.Series(labels).value_counts()
    real_sizes = sizes.drop(index=-1, errors='ignore')

    if real_sizes.empty:
        return {
            'min_cluster_size': 0,
            'max_cluster_size': 0,
            'smallest_cluster_share': 0,
            'largest_cluster_share': 0,
        }

    return {
        'min_cluster_size': int(real_sizes.min()),
        'max_cluster_size': int(real_sizes.max()),
        'smallest_cluster_share': real_sizes.min() / len(labels),
        'largest_cluster_share': real_sizes.max() / len(labels),
    }


def compare_clustering_models(
    df_scaled,
    feature_cols,
    k_range=range(3, 11),
    sample_size=DEFAULT_METRIC_SAMPLE_SIZE,
):
    """Compare K-Means and Ward hierarchical clustering on a reproducible sample."""
    X = _sample_model_data(get_model_matrix(df_scaled, feature_cols), sample_size=sample_size)
    results = []

    for k in k_range:
        models = {
            'kmeans': KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10),
            'hierarchical_ward': AgglomerativeClustering(n_clusters=k, linkage='ward'),
        }

        for model_name, model in models.items():
            labels = model.fit_predict(X)
            metrics = calculate_cluster_metrics(X, labels, sample_size=None)

            results.append({
                'model': model_name,
                'k': k,
                'fit_rows': len(X),
                **metrics,
                **_cluster_size_stats(labels),
            })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'smallest_cluster_share'], ascending=[False, False])
        .reset_index(drop=True)
    )


def compare_kmeans_inertia(df_scaled, feature_cols, k_range=range(1, 11), sample_size=None):
    """
    Calculate K-Means inertia for the elbow method
    """
    X = _sample_model_data(get_model_matrix(df_scaled, feature_cols), sample_size=sample_size)
    results = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10).fit(X)
        results.append({
            'model': 'kmeans',
            'k': k,
            'fit_rows': len(X),
            'inertia': model.inertia_,
        })

    return pd.DataFrame(results)


def compare_dbscan(
    df_scaled,
    feature_cols,
    eps_values=(0.8, 1.0, 1.2, 1.5),
    min_samples_values=(10, 25, 50),
    sample_size=DEFAULT_METRIC_SAMPLE_SIZE,
):
    """Compare DBSCAN settings, mostly to understand density groups and outliers."""
    X = _sample_model_data(get_model_matrix(df_scaled, feature_cols), sample_size=sample_size)
    results = []

    for eps in eps_values:
        for min_samples in min_samples_values:
            labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
            metrics = calculate_cluster_metrics(X, labels, sample_size=None)
            noise_share = (labels == -1).mean()

            results.append({
                'model': 'dbscan',
                'eps': eps,
                'min_samples': min_samples,
                'fit_rows': len(X),
                **metrics,
                'noise_share': noise_share,
                **_cluster_size_stats(labels),
            })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'noise_share'], ascending=[False, True])
        .reset_index(drop=True)
    )


def check_dbscan_outliers(
    df_scaled,
    feature_cols,
    eps_values=(0.8, 1.0, 1.2, 1.5),
    min_samples=25,
    sample_size=DEFAULT_METRIC_SAMPLE_SIZE,
):
    """Use DBSCAN as the professor suggested: mainly to inspect noise/outliers."""
    return compare_dbscan(
        df_scaled,
        feature_cols,
        eps_values=eps_values,
        min_samples_values=(min_samples,),
        sample_size=sample_size,
    )


def compare_mean_shift(df_scaled, feature_cols, quantiles=(0.1, 0.2, 0.3), sample_size=3000):
    """Compare Mean Shift bandwidths estimated from different quantiles."""
    X = _sample_model_data(get_model_matrix(df_scaled, feature_cols), sample_size=sample_size)
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
        metrics = calculate_cluster_metrics(X, labels, sample_size=None)

        results.append({
            'model': 'mean_shift',
            'quantile': quantile,
            'bandwidth': bandwidth,
            'fit_rows': len(X),
            **metrics,
            **_cluster_size_stats(labels),
        })

    return (
        pd.DataFrame(results)
        .sort_values(['silhouette', 'smallest_cluster_share'], ascending=[False, False])
        .reset_index(drop=True)
    )


def fit_final_kmeans(df_scaled, feature_cols, n_clusters):
    """Fit the final K-Means segmentation and return labels plus fitted model."""
    X = get_model_matrix(df_scaled, feature_cols)
    model = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    labels = model.fit_predict(X)
    return labels, model


def compare_kmeans_stability(
    df_scaled,
    feature_cols,
    k_range=range(3, 11),
    seeds=range(10),
    sample_size=DEFAULT_METRIC_SAMPLE_SIZE,
):
    """Check whether K-Means scores are stable across different random seeds."""
    X = _sample_model_data(get_model_matrix(df_scaled, feature_cols), sample_size=sample_size)
    results = []

    for k in k_range:
        for seed in seeds:
            labels = KMeans(n_clusters=k, random_state=seed, n_init=10).fit_predict(X)
            metrics = calculate_cluster_metrics(X, labels, sample_size=None)
            results.append({
                'model': 'kmeans',
                'k': k,
                'seed': seed,
                'fit_rows': len(X),
                **metrics,
                **_cluster_size_stats(labels),
            })

    return (
        pd.DataFrame(results)
        .groupby(['model', 'k'], as_index=False)
        .agg(
            silhouette_mean=('silhouette', 'mean'),
            silhouette_std=('silhouette', 'std'),
            smallest_cluster_share_min=('smallest_cluster_share', 'min'),
            largest_cluster_share_max=('largest_cluster_share', 'max'),
        )
        .sort_values(['silhouette_mean', 'smallest_cluster_share_min'], ascending=[False, False])
        .reset_index(drop=True)
    )


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
        'customer_share': (sizes.values / len(clustered_df)).round(4),
    })


def profile_clusters(clustered_df, profile_cols, cluster_col='cluster'):
    """Create an interpretable segment profile using the unscaled original values."""
    return clustered_df.groupby(cluster_col)[profile_cols].agg(['mean', 'median']).round(2)


def cluster_mean_profile(clustered_df, profile_cols, cluster_col='cluster'):
    """Return cluster means with customer counts and shares in a flat table."""
    profile = clustered_df.groupby(cluster_col)[profile_cols].mean().round(3)
    sizes = cluster_size_summary(clustered_df, cluster_col).set_index(cluster_col)
    return sizes.join(profile).reset_index()


def cluster_lift_profile(clustered_df, profile_cols, cluster_col='cluster'):
    """Compare each cluster mean with the overall mean for easy interpretation."""
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean().replace(0, np.nan)
    lift = cluster_means.divide(overall_means, axis=1).round(3)
    return lift.replace([np.inf, -np.inf], np.nan)


def top_cluster_differences(clustered_df, profile_cols, cluster_col='cluster', top_n=6):
    """List the strongest positive and negative feature differences per cluster."""
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean()
    overall_std = clustered_df[profile_cols].std().replace(0, np.nan)
    z_diffs = cluster_means.subtract(overall_means, axis=1).divide(overall_std, axis=1)

    rows = []
    for cluster_label, values in z_diffs.iterrows():
        values = values.dropna().sort_values()
        for feature, score in values.head(top_n).items():
            rows.append({
                cluster_col: cluster_label,
                'direction': 'below_average',
                'feature': feature,
                'standardized_difference': round(score, 3),
            })
        for feature, score in values.tail(top_n).sort_values(ascending=False).items():
            rows.append({
                cluster_col: cluster_label,
                'direction': 'above_average',
                'feature': feature,
                'standardized_difference': round(score, 3),
            })

    return pd.DataFrame(rows)


def plot_metric_comparison(results):
    """
    Plot the silhouette score used for cluster-count comparison
    """
    plt.figure(figsize=(7, 4))
    sns.lineplot(data=results, x='k', y='silhouette', hue='model', marker='o')
    plt.title('Silhouette score')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette')

    plt.tight_layout()
    plt.show()


def plot_cluster_feature_heatmap(clustered_df, profile_cols, cluster_col='cluster'):
    """
    Plot standardized cluster means to make segment differences easier to see
    """
    cluster_means = clustered_df.groupby(cluster_col)[profile_cols].mean()
    overall_means = clustered_df[profile_cols].mean()
    overall_std = clustered_df[profile_cols].std().replace(0, np.nan)
    heatmap_data = cluster_means.subtract(overall_means, axis=1).divide(overall_std, axis=1)

    plt.figure(figsize=(14, 6))
    sns.heatmap(
        heatmap_data,
        cmap='coolwarm',
        center=0,
        linewidths=0.3,
        linecolor='white',
        cbar_kws={'label': 'Standard deviations from overall mean'},
    )
    plt.title('Cluster profile heatmap')
    plt.xlabel('Feature')
    plt.ylabel('Cluster')
    plt.tight_layout()
    plt.show()


def plot_pca_cluster_map(df_scaled, feature_cols, labels):
    """
    Show clusters in two PCA dimensions for a quick visual sanity check
    """
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
    """
    Show clusters with t-SNE for non-linear visual inspection
    """
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
    """
    Show clusters with UMAP, useful for visual segment separation
    """
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
    """
    Backward-compatible alias for the PCA cluster map
    """
    plot_pca_cluster_map(df_scaled, feature_cols, labels)


def export_customer_clusters(clustered_df, output_path='customer_clusters.csv'):
    """
    Export the required final file: customer_id and proposed cluster
    """
    output = clustered_df[['customer_id', 'cluster']].copy()

    if output['customer_id'].duplicated().any():
        raise ValueError('customer_id appears more than once in the cluster output.')

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    output.to_csv(output_path, index=False)
    return output


def export_cluster_profile(clustered_df, profile_cols, output_path='outputs/cluster_profile.csv'):
    """
    Export a flat cluster profile table for the final report
    """
    output = cluster_mean_profile(clustered_df, profile_cols)

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    output.to_csv(output_path, index=False)
    return output
