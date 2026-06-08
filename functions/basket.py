import ast
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def safe_parse_goods(x):
    if isinstance(x, list):
        return x
    try:
        return ast.literal_eval(x)
    except:
        return []


def generate_association_rules(
    customers,
    basket,
    join_column="customer_id",
    list_column="list_of_goods",
    min_support=0.01,
    metric="lift",
    min_threshold=1,
    min_confidence=0.10
):
    data = basket.merge(
        customers[[join_column]],
        on=join_column,
        how="inner"
    )

    data[list_column] = data[list_column].apply(safe_parse_goods)

    transactions = data[list_column].tolist()
    transactions = [t for t in transactions if len(t) > 0]

    if len(transactions) == 0:
        return pd.DataFrame()

    te = TransactionEncoder()
    encoded = te.fit(transactions).transform(transactions)

    basket_encoded = pd.DataFrame(encoded, columns=te.columns_)

    frequent_itemsets = apriori(
        basket_encoded,
        min_support=min_support,
        use_colnames=True
    )

    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(
        frequent_itemsets,
        metric=metric,
        min_threshold=min_threshold
    )

    rules = rules[rules["confidence"] >= min_confidence]

    return (
        rules[["antecedents", "consequents", "support", "confidence", "lift"]]
        .sort_values("lift", ascending=False)
        .reset_index(drop=True)
    )


def generate_rules_for_all_clusters(
    cluster_dataframes,
    basket,
    params_by_cluster,
    metric="lift",
    default_params=None
):
    if default_params is None:
        default_params = {
            "min_support": 0.01,
            "min_threshold": 1,
            "min_confidence": 0.10
        }

    all_cluster_rules = {}

    for cluster_name, cluster_df in cluster_dataframes.items():

        params = params_by_cluster.get(cluster_name, default_params)

        rules = generate_association_rules(
            customers=cluster_df,
            basket=basket,
            min_support=params["min_support"],
            metric=metric,
            min_threshold=params["min_threshold"],
            min_confidence=params["min_confidence"]
        )

        all_cluster_rules[cluster_name] = rules

    return all_cluster_rules