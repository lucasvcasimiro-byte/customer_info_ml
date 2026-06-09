"""
Apriori Parameter Search - using aulas utils2 approach
-------------------------------------------------------
Mirrors the generate_association_rules from aulas/utils2.py exactly.
Sweeps min_support and min_threshold per cluster and prints recommendations.
"""

import os, sys, warnings, itertools
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")

# project root
def _find_root(start, marker="requirements.txt"):
    p = Path(start).resolve()
    for c in [p] + list(p.parents):
        if (c / marker).exists():
            return str(c)
    raise RuntimeError("Cannot find project root")

ROOT = _find_root(os.path.abspath("."))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# --- load data ----------------------------------------------------------------
print("Loading data...")
customer_basket = pd.read_csv("data/customer_basket.csv")
customer = pd.read_csv("data/ci_clustered.csv")

cluster_dataframes = {
    cluster: group
    for cluster, group in customer.groupby("final_cluster_label")
}
print(f"Clusters: {list(cluster_dataframes.keys())}\n")


# --- exact utils2 implementation ---------------------------------------------
def generate_association_rules(customers, basket,
                               join_column="customer_id",
                               list_column="list_of_goods",
                               min_support=0.2,
                               metric="lift",
                               min_threshold=1):
    data = pd.merge(basket, customers[[join_column]], on=join_column, how="inner")
    transactions = data[list_column].apply(
        lambda x: [item.strip() for item in x[1:-1].split(",")]
    )
    te = TransactionEncoder()
    te_fit = te.fit(transactions).transform(transactions)
    transaction_items = pd.DataFrame(te_fit, columns=te.columns_)

    frequent_itemsets = apriori(transaction_items, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold,
                              num_itemsets=len(frequent_itemsets))
    return rules


# --- grid search --------------------------------------------------------------
# Support range: 0.01 to 0.30 (the aulas notebook uses 0.2 default)
SUPPORT_GRID    = [0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]
THRESHOLD_GRID  = [1.0, 1.1, 1.2, 1.5]   # min lift threshold

results_all = []
best_params = {}

for cluster_name, cluster_df in cluster_dataframes.items():
    n = len(cluster_df)
    print(f"\n{'='*60}")
    print(f"CLUSTER: {cluster_name}  ({n} customers)")

    best_score  = -9999
    best_combo  = None
    best_n_rules = 0

    for ms, mt in itertools.product(SUPPORT_GRID, THRESHOLD_GRID):
        try:
            rules = generate_association_rules(
                cluster_df, customer_basket,
                min_support=ms, metric="lift", min_threshold=mt
            )
        except Exception:
            rules = pd.DataFrame()

        n_rules   = len(rules)
        avg_lift  = rules["lift"].mean() if n_rules > 0 else 0
        avg_conf  = rules["confidence"].mean() if n_rules > 0 else 0

        # scoring: penalise 0 rules and rule explosions; reward lift + confidence
        if n_rules == 0:
            rule_score = -20
        elif n_rules <= 30:
            rule_score = 0
        elif n_rules <= 80:
            rule_score = -0.05 * (n_rules - 30)
        else:
            rule_score = -5 - 0.1 * (n_rules - 80)

        score = avg_lift * 3 + avg_conf * 2 + rule_score

        results_all.append({
            "cluster": cluster_name,
            "min_support": ms,
            "min_threshold": mt,
            "num_rules": n_rules,
            "avg_lift": round(avg_lift, 4),
            "avg_conf": round(avg_conf, 4),
            "score": round(score, 4)
        })

        if score > best_score:
            best_score  = score
            best_combo  = (ms, mt)
            best_n_rules = n_rules

    if best_combo:
        print(f"  Best: min_support={best_combo[0]}, min_threshold={best_combo[1]}")
        print(f"        score={round(best_score,3)} | num_rules={best_n_rules}")
        best_params[cluster_name] = {
            "min_support": best_combo[0],
            "min_threshold": best_combo[1],
        }
    else:
        print("  No valid combo found.")

# --- save results ------------------------------------------------------------
out_dir = Path(ROOT) / "scratch"
out_dir.mkdir(exist_ok=True)

pd.DataFrame(results_all).to_csv(out_dir / "apriori_grid_search.csv", index=False)

summary = pd.DataFrame([
    {"cluster": c, **p} for c, p in best_params.items()
])
summary.to_csv(out_dir / "apriori_best_params.csv", index=False)

# --- print final dict --------------------------------------------------------
print("\n\n" + "="*65)
print("SUMMARY TABLE")
print("="*65)
print(summary.to_string(index=False))

print("\n\n# -- params_by_cluster (paste into notebook) --")
print("params_by_cluster = {")
for cluster, p in best_params.items():
    print(f'    "{cluster}": {{')
    print(f'        "min_support": {p["min_support"]},')
    print(f'        "min_threshold": {p["min_threshold"]},')
    print(f'        "min_confidence": 0.10')
    print("    },")
print("}")
print("\nDone.")
