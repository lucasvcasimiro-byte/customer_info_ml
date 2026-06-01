# Customer Segmentation Project

Machine Learning II project for unsupervised customer segmentation and targeted promotion design.

See [WORKFLOW.md](WORKFLOW.md) for the full project workflow, modeling plan, and submission checklist.

## Setup

```powershell
python -m venv ml2
.\ml2\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Expected Data

- `customer_info.csv`: required for segmentation.
- `customer_basket.csv`: required for association rules and promotion recommendations when available.

## Core Outputs

- `outputs/customer_clusters.csv`: every `customer_id` with its proposed cluster.
- `outputs/cluster_profile.csv`: segment summaries for interpretation.
- `outputs/promotion_recommendations.csv`: campaign ideas backed by basket analysis.

## Working Plan

1. Explore and clean `customer_info.csv`.
2. Engineer interpretable demographic, spend, tenure, promotion, and behavior features.
3. Compare clustering candidates using metrics, stability, and interpretability.
4. Profile final clusters and export the customer-to-cluster CSV.
5. Use `customer_basket.csv` association rules per segment to design targeted promotions.
6. Produce a business-facing report or app without code blocks.

"""
recomendacoes professor:

dbscan is good for outliers (-1 db cluster), not for cluster (2% flag is the reference for this case)

cluster associated with karen behavior

association rules for each cluster (we know 1 of them is vegetarian cluster), tweak parameters for each

use basket for recomendation (cross basket, after clustering), use practical example from week 11 (no train_test_split)

pca not that useful in this project

tsne is good for visualization maybe

use umap for cluster visualization (good definitions)
"""
