import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

from functions.eda import SPEND_COLS

current_year = 2026


# Columns used as features in the clustering model and profiling
NUMERICAL_COLS = [
    # Demographics
    'age',
    'is_female',
    'dependants',
    'education_level',
    'vegetarian',
    'pescatarian',
    'carnivore',
    'omnivore',

    # Buying behaviour
    'has_loyalty_card',
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
    'longitude']



# Updated after eda
FEATURE_COLS =[
        # Demographics
    'age',
    'is_female',
    'dependants',
    'education_level',
    'vegetarian',
    'pescatarian',
    'carnivore',
    'omnivore',

    # Buying behaviour
    'has_loyalty_card',
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',

    # Spending
    'total_spend',

    # Spend shares
    # 'share_groceries',       #Might be removed
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
    'longitude']



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
    Derive dietary preference binary flags based on meat and fish lifetime spend.
    - vegetarian: no meat, no fish
    - pescatarian: no meat, buys fish
    - carnivore: buys meat, no fish
    - omnivore: buys both
    """
    meat = df['lifetime_spend_meat']
    fish = df['lifetime_spend_fish']
    
    df['vegetarian'] = ((meat < 15) & (fish < 15)).astype(int)
    df['pescatarian'] = ((meat < 15) & (fish >= 15)).astype(int)
    df['carnivore'] = ((meat >= 15) & (fish < 15)).astype(int)
    df['omnivore'] = ((meat >= 15) & (fish >= 15)).astype(int)
    
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


# Conjunction of all above
def preprocessing(df_raw):
    """
    Full preprocessing pipeline. Applies every step in order and returns
    a clean dataframe ready for scaling and clustering.

    Steps:
        1. fill_missing_with_zero     - fill NaN complaints, kids, teens, spend with 0
        2. fill_missing_with_median   - fill NaN behavioural cols with median
        3. clean_loyalty_card         - binary has_loyalty_card flag
        4. add_age                    - derive age, drop raw birthdate
        5. add_gender                 - binary is_female flag
        6. add_education              - ordinal education level from name prefix (0–3)
        7. add_dietary_preferences    - binary flags for veg/pescatarian/carnivore/omnivore
        8. add_dependants             - kids_home + teens_home
        9. add_tenure                 - years since first transaction
        10. add_total_spend            - sum of all spend categories
        11. add_spend_shares           - per-category fraction of total spend
        12. check_nulls                - raise if any feature column has NaN
    """
    df = df_raw.copy()

    df = fill_missing_with_zero(df)
    df = fill_missing_with_median(df)
    df = clean_loyalty_card(df)
    df = add_age(df)
    df = add_gender(df)
    df = add_education(df)
    df = add_dietary_preferences(df)
    df = add_dependants(df)
    df = add_tenure(df)
    df = add_total_spend(df)
    df = add_spend_shares(df)

    check_nulls(df, FEATURE_COLS)

    return df


# Scaling
def scale_features(df_features, chosen_scaler):
    """
    Scale FEATURE_COLS with chosen scaler.
    """
    df_scaled = df_features.copy()
    scaler = chosen_scaler()
    df_scaled[FEATURE_COLS] = scaler.fit_transform(df_features[FEATURE_COLS])
    return df_scaled
