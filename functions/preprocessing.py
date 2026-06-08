import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

from functions.eda import SPEND_COLS

current_year = 2026

# All numerical columns
NUMERICAL_COLS = [
    # Demographics
    'age',
    'dependants',
    'education_level',

    # Buying behaviour
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',

    # Spending
    'total_spend',
    'lifetime_spend_groceries',
    'lifetime_spend_electronics',
    'lifetime_spend_vegetables',
    'lifetime_spend_nonalcohol_drinks',
    'lifetime_spend_alcohol_drinks',
    'lifetime_spend_meat',
    'lifetime_spend_fish',
    'lifetime_spend_hygiene',
    'lifetime_spend_videogames',
    'lifetime_spend_petfood',

    # Spend shares
    'share_groceries',
    'share_electronics',
    'share_vegetables',
    'share_nonalcohol_drinks',
    'share_alcohol_drinks',
    'share_meat',
    'share_fish',
    'share_hygiene',
    'share_videogames',
    'share_petfood',
    
    # Location
    'latitude',
    'longitude'
    ]


# Updated after eda
FEATURE_COLS =[
    # Demographics
    'age',
    'dependants',
    'education_level',

    # Buying behaviour
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',

    # Spending
    'total_spend',

    # Spend shares
    #'share_groceries',       
    'share_electronics',
    'share_vegetables',
    'share_nonalcohol_drinks',
    'share_alcohol_drinks',
    'share_meat',
    'share_fish',
    'share_hygiene',
    'share_videogames',
    'share_petfood']


# Preprocessing steps

def fill_missing_with_zero(df):
    """
    Fill missing values with 0 for complaints, household counts, and spend categories
    """
    cols_to_zero = ['number_complaints', 'kids_home', 'teens_home', 'dependants'] + SPEND_COLS
    for col in cols_to_zero:
        df[col] = df[col].fillna(0)
    return df


def fill_missing_with_median(df):
    """
    Fill missing behavioural columns with their median
    """
    for col in ('distinct_stores_visited', 'typical_hour', 'percentage_of_products_bought_promotion', 'age'):
        df[col] = df[col].fillna(df[col].median())
    return df


def clean_loyalty_card(df):
    """
    loyalty_card_number only ever holds value 1; NaN means no card (0)
    """
    df['has_loyalty_card'] = df['loyalty_card_number'].notna().astype(int)
    df = df.drop(columns=['loyalty_card_number'], inplace=True)
    return df


def add_age(df):
    """
    Pass customer_birthdate into age and drop the birthdate column.
    """
    birthdate = pd.to_datetime(
        df['customer_birthdate'], 
        format='mixed', 
        errors='coerce'
    )
    age = current_year - birthdate.dt.year
    df['age'] = age
    df = df.drop(columns=['customer_birthdate'], inplace=True)
    return df


def add_gender(df):
    """
    Binary gender flag where 1 = female and 0 = male
    """
    df['is_female'] = (df['customer_gender'] == 'female').astype(int)
    return df


def add_education(df):
    """
    Ordinal education level extracted from customer_name
    No Degree = 0, Bsc = 1, Msc = 2, Phd = 3
    """
    order = {'No Degree': 0, 'Bsc': 1, 'Msc': 2, 'Phd': 3}
    degree = (
        df['customer_name']
        .str.extract(r'^(Bsc|Msc|Phd)\.', expand=False)
        .fillna('No Degree'))
    df['education_level'] = degree.map(order)
    return df


def add_dietary_preferences(df):
    """
    Derive dietary preference category based on meat, fish, and vegetables spend shares
    """
    meat = df['share_meat']
    fish = df['share_fish']
    veggies = df['share_vegetables']
    
    conditions = [(meat < 0.02) & (fish < 0.02) & (veggies > 0.10),
                (meat < 0.02) & (fish >= 0.10),
                (meat >= 0.10) & (fish < 0.02)]
    choices = ['vegetarian', 'pescatarian', 'carnivore']
    df['dietary_preference'] = np.select(conditions, choices, default = 'omnivore')   
    return df


def add_dependants(df):
    """
    Total dependants at home (kids + teens)
    """
    df['dependants'] = df['kids_home'] + df['teens_home']
    return df


def add_tenure(df):
    """
    Years since first transaction
    """
    df['year_first_transaction'] = df['year_first_transaction'].clip(upper=current_year)
    df['customer_tenure'] = current_year - df['year_first_transaction']
    df['customer_tenure'] = df['customer_tenure'].fillna(df['customer_tenure'].median())
    return df


def add_total_spend(df):
    """
    Sum of all lifetime spend categories
    """
    df['total_spend'] = df[SPEND_COLS].sum(axis=1)
    return df


def add_spend_shares(df):
    """
    Fraction of total spend per category (0 when total_spend is 0)
    """
    for col in SPEND_COLS:
        share_name = 'share_' + col.replace('lifetime_spend_', '')
        df[share_name] = df[col] / df['total_spend'].replace(0, np.nan)
        df[share_name] = df[share_name].fillna(0)
    return df


# Null checking for after preprocessing
def check_nulls(df, cols):
    """
    Raise if any feature column still contains NaN after preprocessing
    """
    missing = df[cols].isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        raise ValueError(f"NaN values remain after preprocessing:\n{missing}")


# Scaling
def scale_features(df_features, chosen_scaler):
    """
    Scale FEATURE_COLS with chosen scaler.
    """
    df_scaled = df_features.copy()
    scaler = chosen_scaler()
    df_scaled[FEATURE_COLS] = scaler.fit_transform(df_features[FEATURE_COLS])
    return df_scaled
