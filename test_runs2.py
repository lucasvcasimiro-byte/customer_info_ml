

import numpy as np
import pandas as pd

from functions.preprocessing import build_features, scale_features, FEATURE_COLS


customer_info   = pd.read_csv('data/customer_info.csv')
customer_basket = pd.read_csv('data/customer_basket.csv')


customer_features        = build_features(customer_info)
customer_scaled, scaler  = scale_features(customer_features)

print(f"Preprocessing concluído: {customer_features.shape[0]} clientes, {len(FEATURE_COLS)} features.")


######## CLUSTERING

from functions.clustering import (compare_clustering_models,fit_final_kmeans,add_clusters,cluster_size_summary,profile_clusters,plot_metric_comparison,plot_pca_cluster_map,plot_umap_cluster_map,export_customer_clusters,compare_dbscan,)

# Comparar K-Means e Hierarchical para k=3,...,10
results = compare_clustering_models(
    customer_scaled,
    FEATURE_COLS,
    k_range=range(3, 11)
)
print('\nClustering model comparison:')
print(results.to_string(index=False))
plot_metric_comparison(results)

# ALTERAR AQUI: escolhe o K depois de veres os resultados das métricas acima.
# Não pode ser automatico tem de ser justificado com base nas métricas, no tamanho dos clusters, e na interpretabilidade de negócio.
best_k = 5

labels, kmeans_model = fit_final_kmeans(customer_scaled, FEATURE_COLS, n_clusters=best_k)
customer_clustered   = add_clusters(customer_features, labels)

print(f'\nSolução K-Means selecionada: k={best_k}')
print('\nTamanho dos clusters:')
print(cluster_size_summary(customer_clustered).to_string(index=False))

# colunas para identificar os clusters
profile_cols = [
    # Demográficas
    'age',
    'is_female',
    'household_size',
    # Comportamento
    'has_loyalty_card',
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'number_complaints',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    # Valor
    'total_spend',
    'spend_per_distinct_product',
    # Shares de categoria 
    'share_groceries',
    'share_electronics',
    'share_vegetables',
    'share_nonalcohol_drinks',
    'share_alcohol_drinks',
    'share_meat',
    'share_fish',
    'share_hygiene',
    'share_videogames',
    'share_petfood',
]

print('\nPerfis dos clusters:')
print(profile_clusters(customer_clustered, profile_cols).to_string())

plot_pca_cluster_map(customer_scaled, FEATURE_COLS, labels)
plot_umap_cluster_map(customer_scaled, FEATURE_COLS, labels)

customer_clusters = export_customer_clusters(customer_clustered)
print('\nExportado customer_clusters.csv')


######## DBSCAN — tratar dos outliers

dbscan_results = compare_dbscan(
    customer_scaled,
    FEATURE_COLS,
    eps_values=(0.8, 1.0, 1.2, 1.5),
    min_samples_values=(10, 25, 50),
)
print('\nResultados DBSCAN:')
print(dbscan_results.to_string(index=False))


