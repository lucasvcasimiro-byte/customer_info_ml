import ast
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def merge_basket_with_clusters(
    customer_basket,
    customer,
    cluster_col='final_cluster_label',
    join_col='customer_id'
):
    return pd.merge(
        customer_basket,
        customer[[join_col, cluster_col]],
        on=join_col,
        how='inner'
    )


def split_by_cluster(df, cluster_col='final_cluster_label'):
    return {
        cluster: group.reset_index(drop=True)
        for cluster, group in df.groupby(cluster_col)
    }


def generate_association_rules_from_cluster(
    cluster_df,
    list_column='list_of_goods',
    min_support=0.02,
    metric='lift',
    min_threshold=1
):
    transactions = cluster_df[list_column].apply(ast.literal_eval)

    transaction_encoder = TransactionEncoder()
    te_array = transaction_encoder.fit(transactions).transform(transactions)

    transaction_items = pd.DataFrame(
        te_array,
        columns=transaction_encoder.columns_
    )

    frequent_itemsets = apriori(
        transaction_items,
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

    if rules.empty:
        return pd.DataFrame()

    if only_simple_rules:
        rules = rules[
            (rules['antecedents'].apply(len) == 1) &
            (rules['consequents'].apply(len) == 1)
        ].copy()

    rules['antecedent_item'] = rules['antecedents'].apply(lambda x: list(x)[0])
    rules['consequent_item'] = rules['consequents'].apply(lambda x: list(x)[0])

    rules['promotion_idea'] = rules.apply(
        lambda row: f"Buy {row['antecedent_item']} and get a discount on {row['consequent_item']}",
        axis=1
    )

    return rules.sort_values('lift', ascending=False).reset_index(drop=True)