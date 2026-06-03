# Customer Segmentation Project Workflow

## Goal

Build a clean, reproducible customer segmentation solution that:

- assigns every `customer_id` in `customer_info.csv` to a final cluster;
- explains what makes each segment distinct;
- uses `customer_basket.csv`, when available, to design realistic promotions per segment;
- keeps reusable code in `.py` files and uses notebooks for exploration, charts, and narrative checkpoints.

## Professor Tips To Respect

- There is a cluster that acts as a Karen
- Use DBSCAN mainly as an outlier/noise diagnostic. Treat the `-1` label as a possible small outlier flag, not as the main segmentation if it only captures a tiny share of customers.
- Use association rules after clustering for each cluster (one is vegetarian), and tweak parameters until good results
- Do not use `train_test_split`; this is unsupervised segmentation, not supervised prediction.
- PCA is useful as a diagnostic, but should not be the main justification if it does not preserve cluster structure well.
- Use t-SNE or UMAP mainly for visualization. UMAP is preferred for showing cluster separation if it gives cleaner definitions.
- Keep the final segmentation practical, interpretable, and marketing-ready.

## Deliverables

- `customer_clusters.csv`: two columns, `customer_id` and `cluster`, with every customer included.
- A report or app with:
  - Executive Summary
  - Exploratory Data Analysis and Pre-Processing
  - Customer Segmentation and Clustering
  - Targeted Promotion
  - Conclusion and Recommendations
- Versionable code in `.py` files.
- Notebook(s) with exploration and evidence, but no large blocks of final business-report code.
- README with setup and run instructions.

## Workflow

### 1. Data Audit

- Load `customer_info.csv`.
- Confirm unique `customer_id`, row count, column types, missing values, duplicate rows, constant columns, and impossible values.
- Drop identifiers and non-informative leakage-like fields from clustering:
  - drop `customer_id` from modeling but keep it for final output;
  - drop `loyalty_card_number` because it is constant;
  - do not use `customer_name` directly, but extract degree level if it is meaningful and stable.
- Convert `customer_birthdate` into `age` and optionally `generation` or `life_stage`.
- Check whether `typical_hour` has many missing values; decide between imputation, missing flag, or exclusion based on missingness.

### 2. Feature Engineering

Create interpretable customer features before clustering:

- `age`
- `household_size_proxy = kids_home + teens_home`
- `customer_tenure = reference_year - year_first_transaction`
- `total_lifetime_spend`
- category spend shares, for example `share_fish`, `share_meat`, `share_electronics`
- value intensity, for example `spend_per_distinct_product`
- promotion sensitivity from `percentage_of_products_bought_promotion`
- store engagement from `distinct_stores_visited`
- complaint behavior from `number_complaints`
- optional geographic features from `latitude` and `longitude`, but only if they improve interpretation.

Keep both raw spend and share features under consideration. Raw spend separates value tiers; shares separate preferences.

### 3. Preprocessing

- Use numeric pipelines with median imputation and `RobustScaler` because spend variables are skewed and outlier-heavy.
- Use one-hot encoding for useful categorical features such as gender and extracted degree level.
- Remove or cap extreme values only when justified by EDA. Prefer robust scaling over aggressive trimming.
- Save a modeling feature list so the final clustering can be reproduced exactly.

### 4. Candidate Models

Fit and compare multiple clustering approaches:

- K-Means or MiniBatchKMeans for a simple baseline.
- Gaussian Mixture Models for soft, potentially elliptical segments.
- Agglomerative clustering for hierarchical structure and dendrogram intuition.
- K-Prototypes only if categorical features are central and the package is allowed/available.
- DBSCAN/HDBSCAN for outlier detection and sanity checks, not as the primary cluster solution unless it gives meaningful segments.

Evaluate a practical range such as `k = 3..10`. Favor a solution that balances score quality, cluster size stability, and interpretability.

### 5. Model Selection

Track:

- silhouette score;
- cluster sizes and tiny-cluster risk;
- stability across random seeds;
- interpretability of profiles.

The selected model should not be chosen by one metric alone. The final answer needs segments that can be named, explained, and acted on.

### 6. Visualization

- Use PCA as a quick diagnostic and to inspect explained variance.
- Use UMAP, or t-SNE if UMAP is unavailable, for 2D cluster visualization.
- Include profile visuals:
  - cluster size bar chart;
  - standardized feature means heatmap;
  - spend-share radar/bar charts;
  - segment comparison table.

### 7. Cluster Profiling

For each cluster, create a profile with:

- size and percentage of customer base;
- demographics: age, gender, family composition;
- value: total spend, tenure, distinct products, store visits;
- category preferences: top spend categories and share differences;
- promotion sensitivity;
- complaints and risk indicators;
- concise business label, for example `High-Value Family Shoppers` or `Promotion-Sensitive Essentials Buyers`.

### 8. Basket And Promotions

When `customer_basket.csv` is available:

- parse `list_of_goods` safely into product lists;
- join basket rows to final customer clusters;
- mine association rules within each cluster;
- tune support/confidence/lift per cluster if some segments have fewer baskets;
- translate rules into feasible campaigns.

Promotion examples should be tied to cluster behavior:

- high meat and fish affinity: cross-sell fish with meat purchases;
- promotion-sensitive customers: basket-level discount or loyalty coupon;
- electronics/video-game affinity: bundle or buy-one-get-one offers;
- family grocery segments: school-week essentials bundles;
- vegetarian/vegetable-heavy segment: fresh produce and non-alcohol drink bundles.

### 9. Final Outputs

- Generate `outputs/customer_clusters.csv`.
- Validate row count equals `customer_info.csv` row count.
- Validate every `customer_id` appears once.
- Generate `outputs/cluster_profile.csv`.
- Generate `outputs/promotion_recommendations.csv` after basket analysis.
- Keep a fixed random seed for reproducibility.

### 10. Report Or App

Use the suggested project index. Keep the report business-facing:

- no code blocks;
- show only necessary charts/tables;
- explain preprocessing decisions briefly;
- justify cluster choice with both metrics and interpretation;
- make promotions creative but plausible.

## Suggested Milestones

- Milestone 1: Finish data audit and preprocessing decisions.
- Milestone 2: Build reusable feature and clustering pipeline in `.py` files.
- Milestone 3: Compare candidate clustering models and select final solution.
- Milestone 4: Produce cluster profiles and final `customer_clusters.csv`.
- Milestone 5: Add basket association rules and segment-specific promotions.
- Milestone 6: Write report or build app, then run final reproducibility checks.

## Quality Checks Before Submission

- `requirements.txt` installs all needed packages in a clean environment.
- Notebook can run top-to-bottom or scripts can regenerate outputs.
- No final deliverable depends on hidden notebook state.
- Final CSV contains every customer exactly once.
- Charts have readable titles, labels, and business interpretation.
- Git history shows meaningful progress before the deadline.
