import numpy as np
import pandas as pd

from utils import *




customer_info = pd.read_csv('data/customer_info.csv')
customer_basket = pd.read_csv('data/customer_basket.csv')

####### muitas visualizacoes para entnder os dados e descobrir insights, deixei pa depois, foquei em experimentar 
####### clustering ja e so fiz preprocessing basico, tem mt a explorar ainda

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

print(customer_info.isnull().sum())


num_cols = customer_info.select_dtypes(include=[np.number]).drop('customer_id', axis=1).columns.tolist()
cat_cols = customer_info.select_dtypes(include=['object', 'string']).columns.tolist()


# Log transformation pq os lifetime_ tao com tail para direita por extremos q gastam mais dinheiro
# Depois de usar, ficou left skewed, tou indeciso se usamos ou n
"""
lifetime_cols = [col for col in num_cols if col.startswith('lifetime_')]

customer_model = customer_info.copy()
customer_model[lifetime_cols] = np.log1p(customer_model[lifetime_cols])
"""

scaler = RobustScaler()
customer_scaled = customer_info.copy()
customer_scaled[num_cols] = scaler.fit_transform(customer_info[num_cols])






