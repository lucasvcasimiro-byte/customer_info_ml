import os
import ast
import json
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)

# 1. Caminhos de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CLUSTERING_FILE = os.path.join(DATA_DIR, 'ci_clustering.csv')
BASKET_FILE = os.path.join(DATA_DIR, 'customer_basket.csv')
RULES_FILE = os.path.join(DATA_DIR, 'cluster_association_rules.json')

# 2. Carregar e indexar dados dos clientes
print("A carregar base de dados de clientes (ci_clustering.csv)...")
df_ci = pd.read_csv(CLUSTERING_FILE)
print(f"Carregados {len(df_ci)} clientes com sucesso!")

# Colunas de características (features)
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

print("A normalizar características...")
scaler = StandardScaler()
X = scaler.fit_transform(df_ci[FEATURE_COLS])

print("A treinar modelo K-Means (K=6)...")
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
df_ci['cluster'] = kmeans.fit_predict(X)
print("Treino concluído com sucesso!")

# Indexar base de dados de clientes para lookup instantâneo
customer_lookup = {}
for index, row in df_ci.iterrows():
    cid = str(int(row['customer_id']))
    customer_lookup[cid] = row

# 3. Carregar e indexar cestas de compras
print("A carregar cestas de compras (customer_basket.csv)...")
df_basket = pd.read_csv(BASKET_FILE)
invoice_lookup = {}
customer_baskets = {}

for index, row in df_basket.iterrows():
    inv_id = str(int(row['invoice_id']))
    cust_id = str(int(row['customer_id']))
    try:
        goods = ast.literal_eval(row['list_of_goods'])
    except:
        goods = []
    
    invoice_lookup[inv_id] = {
        'customer_id': cust_id,
        'goods': goods
    }
    
    if cust_id not in customer_baskets:
        customer_baskets[cust_id] = []
    customer_baskets[cust_id].append({
        'invoice_id': inv_id,
        'goods': goods
    })

# Ordenar as transações de cada cliente por ID de fatura descendente (mais recente primeiro)
for cust_id in customer_baskets:
    customer_baskets[cust_id].sort(key=lambda x: int(x['invoice_id']), reverse=True)
print("Cestas indexadas com sucesso!")

# 4. Carregar regras de associação dos clusters
print("A carregar regras de associação dos clusters...")
if os.path.exists(RULES_FILE):
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        cluster_rules = json.load(f)
    print("Regras de associação carregadas com sucesso!")
else:
    print("AVISO: Ficheiro de regras não encontrado. A inicializar vazio.")
    cluster_rules = {str(i): [] for i in range(6)}

# 5. Mapeamento estrito dos clusters com base na análise de centróides
# campaignItems = itens sobre os quais o desconto se aplica (devem bater com nextBestOffer)
# items         = itens default de fallback para cross-selling (da análise de cestas)
CLUSTER_SEGMENTS = {
    0: {
        'segment': 'Younger Promo-Sensitive Shoppers',
        'discount': '25%',
        'nextBestOffer': '25% off Next Promotional Visit',
        'campaignItems': ['fresh bread', 'milk', 'eggs'],          # itens com desconto
        'items': ['asparagus', 'airpods', 'tomatoes'],             # fallback cross-sell
        'propensity': 0.82
    },
    1: {
        'segment': 'Vegetable Heavy / Healthy Shoppers',
        'discount': '15%',
        'nextBestOffer': '15% off Organic Vegetables Subscription',
        'campaignItems': ['asparagus', 'spinach', 'tomatoes'],     # itens com desconto (vegetais)
        'items': ['dog food', 'babies food', 'napkins'],           # fallback cross-sell
        'propensity': 0.88
    },
    2: {
        'segment': 'Premium Large Families',
        'discount': '15%',
        'nextBestOffer': 'Bundle: School-Week Groceries (save €5.00)',
        'campaignItems': ['cereals', 'fresh bread', 'milk'],       # itens com desconto
        'items': ['butter', 'eggs', 'oatmeal'],                   # fallback cross-sell
        'propensity': 0.91
    },
    3: {
        'segment': 'Diet-Specific (Non-Omnivores)',
        'discount': '10%',
        'nextBestOffer': '10% off Fresh Fish & Meat Packs',
        'campaignItems': ['salmon', 'chicken', 'bacon'],           # itens com desconto
        'items': ['babies food', 'dog food', 'cooking oil'],       # fallback cross-sell
        'propensity': 0.76
    },
    4: {
        'segment': 'Groceries Heavy Omnivores',
        'discount': '12%',
        'nextBestOffer': '12% off Groceries Bundle',
        'campaignItems': ['fresh bread', 'butter', 'eggs'],        # itens com desconto
        'items': ['airpods', 'asparagus', 'bluetooth headphones'], # fallback cross-sell
        'propensity': 0.85
    },
    5: {
        'segment': 'Late-Hour & Hygiene Shoppers',
        'discount': '10%',
        'nextBestOffer': '10% off Electronics Flash Sale (after 18:00)',
        'campaignItems': ['shampoo', 'toothpaste', 'deodorant'],   # itens com desconto
        'items': ['energy bar', 'protein bar', 'antioxydant juice'],# fallback cross-sell
        'propensity': 0.79
    }
}

# 6. Lógica de recomendação híbrida
def recommend_items(cluster_idx, basket_items):
    basket_set = set(item.lower() for item in basket_items)
    matched_consequents = []
    
    # Camada 1: Regras do próprio cluster
    rules = cluster_rules.get(str(cluster_idx), [])
    for rule in rules:
        antecedents = set(item.lower() for item in rule['antecedents'])
        if antecedents.issubset(basket_set):
            for item in rule['consequents']:
                item_clean = item.strip()
                if item_clean.lower() not in basket_set and item_clean not in matched_consequents:
                    matched_consequents.append(item_clean)
                    
    # Camada 2: Regras dos outros clusters (caso falte recomendações)
    if len(matched_consequents) < 3:
        for c_id in range(6):
            if c_id == cluster_idx:
                continue
            other_rules = cluster_rules.get(str(c_id), [])
            for rule in other_rules:
                antecedents = set(item.lower() for item in rule['antecedents'])
                if antecedents.issubset(basket_set):
                    for item in rule['consequents']:
                        item_clean = item.strip()
                        if item_clean.lower() not in basket_set and item_clean not in matched_consequents:
                            matched_consequents.append(item_clean)
                            
    # Filtrar para garantir unicidade case-insensitive
    final_recs = []
    seen_lower = set()
    for item in matched_consequents:
        if item.lower() not in seen_lower:
            final_recs.append(item)
            seen_lower.add(item.lower())
            
    # Camada 3: Preencher com os populares por defeito do cluster
    defaults = CLUSTER_SEGMENTS[cluster_idx]['items']
    for item in defaults:
        if len(final_recs) >= 3:
            break
        if item.lower() not in basket_set and item.lower() not in seen_lower:
            final_recs.append(item)
            seen_lower.add(item.lower())
            
    # Camada 4: Fallback absoluto global
    fallback_items = ['Milk', 'Fresh Bread', 'Butter', 'Eggs']
    for item in fallback_items:
        if len(final_recs) >= 3:
            break
        if item.lower() not in basket_set and item.lower() not in seen_lower:
            final_recs.append(item)
            seen_lower.add(item.lower())
            
    return final_recs[:3]

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    cid_raw = request.args.get('customer_id', '')
    if not cid_raw:
        return jsonify({'error': 'customer_id is required'}), 400
    
    # Limpar input
    query_val = cid_raw.strip()
    if query_val.upper().startswith('C'):
        query_val = query_val[1:]
    
    # Determinar se a pesquisa é por ID de Fatura (invoice) ou ID de Cliente (customer)
    basket_found = None
    invoice_id = None
    customer_id = None
    
    # 1. Verificar se é uma fatura
    if query_val in invoice_lookup:
        inv_data = invoice_lookup[query_val]
        invoice_id = query_val
        customer_id = inv_data['customer_id']
        basket_found = inv_data['goods']
        print(f"Lookup por Fatura: {invoice_id} -> Cliente: {customer_id}, Itens: {basket_found}")
    else:
        # Se não for fatura, tentar converter para ID de cliente
        try:
            customer_id = str(int(query_val))
        except ValueError:
            return jsonify({'notFound': True, 'error': 'ID de cliente/fatura inválido'}), 404
            
        # Obter cesta mais recente do cliente
        if customer_id in customer_baskets and len(customer_baskets[customer_id]) > 0:
            latest = customer_baskets[customer_id][0]
            invoice_id = latest['invoice_id']
            basket_found = latest['goods']
            print(f"Lookup por Cliente: {customer_id} -> Fatura mais recente: {invoice_id}, Itens: {basket_found}")
        else:
            basket_found = []
            invoice_id = "N/A"
            print(f"Lookup por Cliente: {customer_id} -> Sem transações registadas.")

    # 2. Obter perfil do cliente para a segmentação
    if customer_id not in customer_lookup:
        return jsonify({'notFound': True, 'error': f'Cliente ID {cid_raw} não encontrado'}), 404
        
    row = customer_lookup[customer_id]
    cluster_idx = int(row['cluster'])
    profile = CLUSTER_SEGMENTS[cluster_idx]
    
    # 3. Lógica adaptativa em tempo real com base no cesto de compras
    segment_name = profile['segment']
    next_best_offer = profile['nextBestOffer']
    
    basket_lower = [item.lower() for item in basket_found]
    has_meat = any(x in basket_lower for x in ['ground beef', 'chicken', 'salmon', 'bacon', 'beef', 'fish', 'shrimp', 'pork'])
    has_electronics = any(x in basket_lower for x in ['ring light', 'airpods', 'headphones', 'earbuds', 'samsung', 'galaxy', 'iphone'])
    
    # Adaptação dinâmica para o Cluster 1 (Vegetable Heavy)
    campaign_items = profile['campaignItems'][:]
    if cluster_idx == 1:
        if has_meat:
            segment_name = 'Vegetable Heavy / Flexitarian'
            next_best_offer = '15% off Fresh Produce & Protein Bundle'
            campaign_items = ['asparagus', 'salmon', 'chicken']   # vegetais + proteína
        elif has_electronics:
            segment_name = 'Healthy Tech Shopper'
            next_best_offer = '15% off Smart Kitchen & Fresh Produce'
            campaign_items = ['asparagus', 'spinach', 'tomatoes']
            
    # 4. Calcular itens de cross-sell via regras de associação
    cross_sell_items = recommend_items(cluster_idx, basket_found)
    
    # 5. Construir resposta combinada
    response = {
        'customerId': customer_id,
        'invoiceId': invoice_id,
        'customerName': str(row['customer_name']),
        'customerGender': str(row['customer_gender']),
        'age': int(row['age']),
        'segment': segment_name,
        'discount': profile['discount'],
        'nextBestOffer': next_best_offer,
        'basket': basket_found,
        'campaignItems': campaign_items,         # itens sobre os quais o desconto se aplica
        'items': cross_sell_items,               # sugestões adicionais de cross-selling
        'propensity': float(row['percentage_of_products_bought_promotion'] if cluster_idx == 0 else profile['propensity']),
        'totalSpend': float(row['total_spend']),
        'algorithm': 'K-Means (K=6) + Apriori (Real-Time)'
    }
    return jsonify(response)

if __name__ == '__main__':
    print("A iniciar o servidor Flask em http://localhost:5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
