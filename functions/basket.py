import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import ast


def generate_association_rules(
    data,
    list_column="list_of_goods",
    min_support=0.05,
    metric="lift",
    min_threshold=1.0,
):
    """
    Generate association rules for a given DataFrame of transactions.
    """

    # Simple string-split parse (same as aulas/utils2.py)
    transactions = data[list_column].apply(ast.literal_eval)

    te = TransactionEncoder()
    te_fit = te.fit(transactions).transform(transactions)
    transaction_items = pd.DataFrame(te_fit, columns=te.columns_)

    frequent_itemsets = apriori(transaction_items, min_support=min_support, use_colnames=True)

    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(
        frequent_itemsets,
        metric=metric,
        min_threshold=min_threshold,
        num_itemsets=len(frequent_itemsets),
    )

    return rules.sort_values("lift", ascending=False).reset_index(drop=True)


def generate_rules_for_all_clusters(
    cluster_dataframes,
    params_by_cluster,
    metric="lift",
    default_params=None,
):
    """
    Run generate_association_rules for every cluster, using per-cluster params.
    """
    if default_params is None:
        default_params = {
            "min_support": 0.05,
            "min_threshold": 1.0,
        }

    all_cluster_rules = {}

    for cluster_name, cluster_df in cluster_dataframes.items():
        params = params_by_cluster.get(cluster_name, default_params)

        rules = generate_association_rules(
            data=cluster_df,
            min_support=params["min_support"],
            metric=metric,
            min_threshold=params["min_threshold"],
        )

        all_cluster_rules[cluster_name] = rules

    return all_cluster_rules