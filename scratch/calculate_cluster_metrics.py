import pandas as pd
import numpy as np

# Load data
df_ci = pd.read_csv("data/ci_clustered.csv")
df_basket = pd.read_csv("data/customer_basket.csv")

# Count invoices per customer
basket_counts = df_basket.groupby('customer_id').size().rename('invoice_count')
df_ci = df_ci.merge(basket_counts, left_on='customer_id', right_index=True, how='left')
df_ci['invoice_count'] = df_ci['invoice_count'].fillna(0)

# Calculate global min/max for normalization
spend_min, spend_max = df_ci['total_spend'].min(), df_ci['total_spend'].max()
inv_min, inv_max = df_ci['invoice_count'].min(), df_ci['invoice_count'].max()
variety_min, variety_max = df_ci['lifetime_total_distinct_products'].min(), df_ci['lifetime_total_distinct_products'].max()
promo_min, promo_max = df_ci['percentage_of_products_bought_promotion'].min(), df_ci['percentage_of_products_bought_promotion'].max()

# Let's define recency proxy: higher max invoice ID means more recent.
# Let's find the maximum invoice_id overall, and the max invoice_id for each customer.
max_inv_overall = df_basket['invoice_id'].max()
cust_max_inv = df_basket.groupby('customer_id')['invoice_id'].max()
df_ci = df_ci.merge(cust_max_inv.rename('max_invoice_id'), left_on='customer_id', right_index=True, how='left')
# Recency proxy: lower max invoice ID means higher recency (days ago).
# Let's scale it so that it ranges from, say, 2 days to 60 days.
min_max_inv, max_max_inv = df_ci['max_invoice_id'].min(), df_ci['max_invoice_id'].max()
df_ci['recency_days'] = 2 + 58 * (1 - (df_ci['max_invoice_id'] - min_max_inv) / (max_max_inv - min_max_inv + 1))
recency_min, recency_max = df_ci['recency_days'].min(), df_ci['recency_days'].max()

print("Global ranges:")
print(f"Total Spend: {spend_min} - {spend_max}")
print(f"Invoice count: {inv_min} - {inv_max}")
print(f"Variety: {variety_min} - {variety_max}")
print(f"Promo: {promo_min} - {promo_max}")
print(f"Recency: {recency_min} - {recency_max}")

# We will scale each feature to 0-100 for the radar chart based on the cluster means relative to each other, or relative to the global distribution.
# Let's compute the cluster means first.
cluster_groups = df_ci.groupby(['final_cluster_nr', 'final_cluster_label'])

cluster_data_list = []

for (cid, clabel), c_df in sorted(cluster_groups, key=lambda x: x[0][0]):
    count = len(c_df)
    pct = count / len(df_ci) * 100
    avg_spend = c_df['total_spend'].mean()
    avg_invoices = c_df['invoice_count'].mean()
    avg_recency = c_df['recency_days'].mean()
    avg_variety = c_df['lifetime_total_distinct_products'].mean()
    avg_promo = c_df['percentage_of_products_bought_promotion'].mean()
    avg_age = c_df['age'].mean()
    avg_dep = c_df['dependants'].mean()
    avg_complaints = c_df['number_complaints'].mean()
    
    cluster_data_list.append({
        'id': int(cid),
        'name': clabel,
        'count': count,
        'percentage': round(pct, 1),
        'avgSpend_raw': avg_spend,
        'avgInvoices_raw': avg_invoices,
        'avgRecency_raw': avg_recency,
        'avgVariety_raw': avg_variety,
        'avgPromo_raw': avg_promo,
        'avgAge': round(avg_age, 1),
        'avgDep': round(avg_dep, 2),
        'avgComplaints': round(avg_complaints, 2)
    })

# Now let's print the raw values and normalize them for radar
# Normalize functions: scale means to 0-100 based on the min/max of the cluster averages to show contrast
min_spend_mean = min(c['avgSpend_raw'] for c in cluster_data_list)
max_spend_mean = max(c['avgSpend_raw'] for c in cluster_data_list)

min_inv_mean = min(c['avgInvoices_raw'] for c in cluster_data_list)
max_inv_mean = max(c['avgInvoices_raw'] for c in cluster_data_list)

min_rec_mean = min(c['avgRecency_raw'] for c in cluster_data_list)
max_rec_mean = max(c['avgRecency_raw'] for c in cluster_data_list)

min_var_mean = min(c['avgVariety_raw'] for c in cluster_data_list)
max_var_mean = max(c['avgVariety_raw'] for c in cluster_data_list)

min_promo_mean = min(c['avgPromo_raw'] for c in cluster_data_list)
max_promo_mean = max(c['avgPromo_raw'] for c in cluster_data_list)

print("\n--- Calculated cluster parameters for UI ---")
for c in cluster_data_list:
    # Scale between 15 and 98 to keep the radar chart nice and readable
    def scale_radar(val, min_val, max_val, invert=False):
        if max_val == min_val:
            return 50
        norm = (val - min_val) / (max_val - min_val)
        if invert:
            norm = 1 - norm
        return int(15 + 83 * norm)
        
    spending_score = scale_radar(c['avgSpend_raw'], min_spend_mean, max_spend_mean)
    frequency_score = scale_radar(c['avgInvoices_raw'], min_inv_mean, max_inv_mean)
    # Recency: lower recency_days means more recent, so higher score!
    recency_score = scale_radar(c['avgRecency_raw'], min_rec_mean, max_rec_mean, invert=True)
    variety_score = scale_radar(c['avgVariety_raw'], min_var_mean, max_var_mean)
    promo_score = scale_radar(c['avgPromo_raw'], min_promo_mean, max_promo_mean)
    
    # Format for UI display
    # Assume 1 invoice = 1 visit. Average frequency per month is avgInvoices_raw / 12 (since tenure is in months, wait, tenure is in what units?)
    # Let's check average customer tenure: it is around 10 months. So avgInvoices / tenure would be monthly visits.
    tenure_mean = df_ci[df_ci['final_cluster_nr'] == c['id']]['customer_tenure'].mean()
    freq_mo = c['avgInvoices_raw'] / (tenure_mean if tenure_mean > 0 else 12)
    
    print(f"\nID: {c['id']}, Name: '{c['name']}'")
    print(f"  Count: {c['count']}, Percentage: {c['percentage']}%")
    print(f"  Avg Spend: €{c['avgSpend_raw']:.2f} -> display: '€{int(c['avgSpend_raw']):,}'")
    print(f"  Avg Invoices: {c['avgInvoices_raw']:.2f}, Tenure: {tenure_mean:.1f} months -> Freq/mo: {freq_mo:.1f} -> display: '{freq_mo:.1f}×/mo'")
    print(f"  Avg Recency Days: {c['avgRecency_raw']:.1f} -> display: '{int(c['avgRecency_raw'])} days'")
    print(f"  Avg Complaints: {c['avgComplaints']}")
    print(f"  Radar: {{ Spending: {spending_score}, Frequency: {frequency_score}, Recency: {recency_score}, Variety: {variety_score}, PromotionSensitivity: {promo_score} }}")
