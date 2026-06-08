import os
import ast
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 1. Carregar dados de clientes e determinar clusters
print("A carregar ci_clustering.csv...")
df_ci = pd.read_csv('data/ci_clustering.csv')

FEATURE_COLS = [
    'age', 'is_female', 'dependants', 'education_level',
    'vegetarian', 'pescatarian', 'carnivore', 'omnivore',
    'has_loyalty_card', 'customer_tenure', 'distinct_stores_visited',
    'typical_hour', 'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products', 'number_complaints',
    'total_spend',
    'share_groceries', 'share_electronics', 'share_vegetables',
    'share_nonalcohol_drinks', 'share_alcohol_drinks', 'share_meat',
    'share_fish', 'share_hygiene', 'share_videogames', 'share_petfood',
    'latitude', 'longitude'
]

scaler = StandardScaler()
X = scaler.fit_transform(df_ci[FEATURE_COLS])
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
df_ci['cluster'] = kmeans.fit_predict(X)

# Mapear customer_id -> cluster
customer_cluster_map = dict(zip(df_ci['customer_id'].astype(int), df_ci['cluster'].astype(int)))

# 2. Carregar cestas de compras
print("A carregar customer_basket.csv...")
df_basket = pd.read_csv('data/customer_basket.csv')

# Mapear cesta -> cluster
df_basket['cluster'] = df_basket['customer_id'].map(customer_cluster_map)
# Filtrar nulos (casos onde o cliente na cesta não existe no clustering)
df_basket = df_basket.dropna(subset=['cluster'])
df_basket['cluster'] = df_basket['cluster'].astype(int)

# Converter list_of_goods de string para lista de Python
print("A processar listas de compras...")
def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except:
        return []

df_basket['goods_list'] = df_basket['list_of_goods'].apply(safe_eval)

# 3. Minar regras por cluster
cluster_rules = {}

for cluster_id in range(6):
    print(f"\n--- A processar Cluster {cluster_id} ---")
    df_cluster = df_basket[df_basket['cluster'] == cluster_id]
    baskets = df_cluster['goods_list'].tolist()
    print(f"Número de transações no Cluster {cluster_id}: {len(baskets)}")
    
    if len(baskets) < 10:
        print("Poucas transações para minar regras.")
        cluster_rules[str(cluster_id)] = []
        continue
        
    # Usar TransactionEncoder
    te = TransactionEncoder()
    te_ary = te.fit(baskets).transform(baskets)
    df_te = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Executar Apriori com min_support dinâmico ou fixo (0.01 por defeito)
    # Tenta obter uma quantidade razoável de regras
    min_sup = 0.01
    frequent_itemsets = apriori(df_te, min_support=min_sup, use_colnames=True)
    
    # Se existirem poucos itemsets, tentar reduzir min_support para capturar regras
    if len(frequent_itemsets) < 5 and min_sup > 0.002:
        min_sup = 0.002
        print(f"Poucos itemsets frequentes. A reduzir min_support para {min_sup}")
        frequent_itemsets = apriori(df_te, min_support=min_sup, use_colnames=True)
        
    print(f"Itemsets frequentes encontrados: {len(frequent_itemsets)}")
    
    if len(frequent_itemsets) == 0:
        cluster_rules[str(cluster_id)] = []
        continue
        
    # Gerar regras de associação
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    print(f"Regras geradas: {len(rules)}")
    
    # Se não houver regras com lift > 1, reduzir o threshold do lift ou usar confiança
    if len(rules) == 0:
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
        print(f"Regras geradas com base em confiança: {len(rules)}")
        
    # Ordenar por lift decrescente
    rules = rules.sort_values(by='lift', ascending=False)
    
    # Converter para dicionário serializável em JSON
    formatted_rules = []
    # Limitar às top 50 regras por cluster para não sobrecarregar
    for _, row in rules.head(50).iterrows():
        formatted_rules.append({
            'antecedents': list(row['antecedents']),
            'consequents': list(row['consequents']),
            'support': float(row['support']),
            'confidence': float(row['confidence']),
            'lift': float(row['lift'])
        })
        
    cluster_rules[str(cluster_id)] = formatted_rules

# Salvar no ficheiro JSON
output_file = 'data/cluster_association_rules.json'
print(f"\nA gravar regras em {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cluster_rules, f, ensure_ascii=False, indent=2)
print("Concluído!")
