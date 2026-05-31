import numpy as np
import pandas as pd

from utils import *
from preprocessing import build_features, scale_features, FEATURE_COLS

####### LOADUING DATA

customer_info = load_data('data/customer_info.csv')
customer_basket = load_data('data/customer_basket.csv')

####### preprocessamento das conclusoes, para ser usavel no clustering

# Fill Loyalty Card with 0 (Boolean flag) - so havia 1 valor, que era 1, portanto assumi que NaN = No Loyalty Card = 0
customer_info['loyalty_card_number'] = customer_info['loyalty_card_number'].fillna(0)

# Fill Number of Complaints with 0 (Assumption: No record = No complaint)
customer_info['number_complaints'] = customer_info['number_complaints'].fillna(0)

# Convert Birthdate to Age, then fill missing ages with Median
customer_info['customer_birthdate'] = pd.to_datetime(customer_info['customer_birthdate'], format='%m/%d/%Y %I:%M %p')
customer_info['age'] = 2025 - customer_info['customer_birthdate'].dt.year 
customer_info['age'] = customer_info['age'].fillna(customer_info['age'].median())
customer_info = customer_info.drop(columns=['customer_birthdate']) 

# Fill all remaining numerical columns with their respective Median, safety
cols_to_fill_median = [
    'kids_home', 'teens_home', 'distinct_stores_visited', 'typical_hour',
    'lifetime_spend_electronics', 'lifetime_spend_vegetables', 
    'lifetime_spend_alcohol_drinks', 'lifetime_spend_meat', 
    'lifetime_spend_fish', 'lifetime_spend_hygiene', 
    'lifetime_spend_videogames', 'lifetime_spend_petfood',
    'percentage_of_products_bought_promotion'
]

for col in cols_to_fill_median:
    customer_info[col] = customer_info[col].fillna(customer_info[col].median())

num_cols = customer_info.select_dtypes(include=[np.number]).drop('customer_id', axis=1).columns.tolist()
cat_cols = customer_info.select_dtypes(include=['object', 'string']).columns.tolist()


scaler = RobustScaler()
customer_scaled = customer_info.copy()
customer_scaled[num_cols] = scaler.fit_transform(customer_info[num_cols])

######## CLUSTERING

from clustering import *

# Check which scaled modeling features still have missing values.
# clustering.py will median-impute them before fitting the models.
missing_summary = customer_scaled[num_cols].isnull().sum().reset_index()
print('\nMissing values in model features:')
print(missing_summary.head(10).to_string(index=False))

# Compare the course-approved cluster-count methods:
# K-Means and hierarchical clustering.
results = compare_clustering_models(
    customer_scaled,
    num_cols,
    k_range=range(3, 11)
)
print('\nClustering model comparison:')
print(results.to_string(index=False))
plot_metric_comparison(results)

# Pick the best K-Means result as a first candidate.
# We keep K-Means as the final model because it assigns every customer to a segment
# and is easy to explain for marketing strategy.
kmeans_results = results[results['model'] == 'kmeans'].copy()
best_k = int(kmeans_results.iloc[0]['k'])

labels, kmeans_model = fit_final_kmeans(customer_scaled, num_cols, n_clusters=best_k)
customer_clustered = add_clusters(customer_info, labels)

print(f'\nSelected initial K-Means solution: k={best_k}')
print('\nCluster sizes:')
print(cluster_size_summary(customer_clustered).to_string(index=False))

profile_cols = [
    'kids_home',
    'teens_home',
    'number_complaints',
    'distinct_stores_visited',
    'lifetime_spend_groceries',
    'lifetime_spend_electronics',
    'lifetime_spend_vegetables',
    'lifetime_spend_nonalcohol_drinks',
    'lifetime_spend_alcohol_drinks',
    'lifetime_spend_meat',
    'lifetime_spend_fish',
    'lifetime_spend_hygiene',
    'lifetime_spend_petfood',
    'lifetime_spend_videogames',
    'lifetime_total_distinct_products',
    'percentage_of_products_bought_promotion',
    'year_first_transaction',
]

print('\nCluster profiles:')
print(profile_clusters(customer_clustered, profile_cols).to_string())

plot_pca_cluster_map(customer_scaled, num_cols, labels)

customer_clusters = export_customer_clusters(customer_clustered)
print('\nExported customer_clusters.csv')


######## OPTIONAL COURSE METHODS

# DBSCAN is useful to inspect density-based groups and noise/outliers.
# Uncomment if you want to compare DBSCAN settings.
"""
dbscan_results = compare_dbscan(
    customer_scaled,
    num_cols,
    eps_values=(0.8, 1.0, 1.2, 1.5),
    min_samples_values=(10, 25, 50),
)
print(dbscan_results.to_string(index=False))
"""

# Mean Shift can be slow on this dataset. Use a sample first if you test it.
"""
mean_shift_results = compare_mean_shift(
    customer_scaled,
    num_cols,
    quantiles=(0.1, 0.2, 0.3),
    sample_size=3000,
)
print(mean_shift_results.to_string(index=False))
"""

# UMAP can give a better non-linear visualization than PCA, but it takes longer.
"""
plot_umap_cluster_map(customer_scaled, num_cols, labels)
"""