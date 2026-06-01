import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

from functions.eda import SPEND_COLS

current_year=2026


# Columns that will be used as features in the clustering model and profiling
FEATURE_COLS = [
    # Demographics 
    'age',
    'is_female',
    'household_size',
    # Checkem as colunas de educação, acho que devemos retirar, mas deixo aqui para experimentarmos com e sem
    #'edu_Bsc',
    #'edu_Msc',
    #'edu_Phd',

    # Buying behavior
    'has_loyalty_card',
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',

    # Spendings  
    'total_spend',
    #'spend_per_distinct_product',

    # Shares    
    'share_groceries',
    'share_electronics',
    'share_vegetables',
    'share_nonalcohol_drinks',
    'share_alcohol_drinks',
    'share_meat',
    'share_fish',
    'share_hygiene',
    'share_videogames',
    'share_petfood']


def check_nulls(df: pd.DataFrame, cols: list):
    """
    Verify if there's nulls in specified columns, to confirm that 
    preprocessing worked as expected
    
    """
    missing = df[cols].isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        raise ValueError(
            f"There's NaN after preprocessing:\n{missing}")




def preprocessing(df_raw: pd.DataFrame):
    """
    Receives the customer_info.csv dataframe and returns a new preprocessed one 
    with the new features included (no scaling included)
    """
    df = df_raw.copy()
    
    # Cleans existing columns
    
    #  Assuming NaN means there's no registered complaint
    df['number_complaints'] = df['number_complaints'].fillna(0)

    #  loyalty_card_number only has value 1, so we assume Nan means no loyalty card (binary column)
    df['has_loyalty_card'] = df['loyalty_card_number'].notna().astype(int)

    #  2026-2029
    df['year_first_transaction'] = df['year_first_transaction'].clip(upper=current_year)

    #  Considering NaN as 0 (assumimg there's no kids/teens at home)
    df['kids_home'] = df['kids_home'].fillna(0)
    df['teens_home'] = df['teens_home'].fillna(0)

    #  Replacing missing values with median
    df['distinct_stores_visited'] = df['distinct_stores_visited'].fillna(df['distinct_stores_visited'].median())
    df['typical_hour'] = df['typical_hour'].fillna(df['typical_hour'].median())
    df['percentage_of_products_bought_promotion'] = df['percentage_of_products_bought_promotion'].fillna(
        df['percentage_of_products_bought_promotion'].median())

    # In columns with missing values, we assume that NaN means 0 spend
    for col in SPEND_COLS:
        df[col] = df[col].fillna(0)

    # Age from birthdate, assuming invalid/missing dates mean median age (invalid dates become NaN in age)
    df['customer_birthdate'] = pd.to_datetime(df['customer_birthdate'],
        format='%m/%d/%Y %I:%M %p',
        errors='coerce' )
    
    df['age'] = current_year - df['customer_birthdate'].dt.year
    df['age'] = df['age'].fillna(df['age'].median())  

    # Drop birthdate after extracting age
    df = df.drop(columns=['customer_birthdate'])

    # Gender, 1 = female, 0 = male
    df['is_female'] = (df['customer_gender'] == 'female').astype(int)


######## Acho q deviamos apagar a parte da educacao, mas deixo assim pa experimentarmos com e sem

    # Academic degree from customer_name
#    df['education_level'] = (
 #       df['customer_name']
  #      .str.extract(r'^(Bsc|Msc|Phd)\.', expand=False)
   #     .fillna('No_Degree')
    #)
    
    #edu_dummies = pd.get_dummies(
     #   df['education_level'],
      #  prefix='edu',
       # drop_first=False,
        #dtype=int
    #)
    #df = pd.concat([df, edu_dummies], axis=1)  

    # Number of people at home
    df['household_size'] = df['kids_home'] + df['teens_home']

    # Customer tenure (years since first transaction)
    df['customer_tenure'] = current_year - df['year_first_transaction']
    df['customer_tenure'] = df['customer_tenure'].fillna(df['customer_tenure'].median())

    # Total spend across all categories
    df['total_spend'] = df[SPEND_COLS].sum(axis=1)

    # percentagem de cada categoria no total
    
    for col in SPEND_COLS:
        share_name = 'share_' + col.replace('lifetime_spend_', '')
        df[share_name] = df[col] / df['total_spend'].replace(0, np.nan)
        df[share_name] = df[share_name].fillna(0)


    #### Esta parte tambem deviamos tentar com e sem, parece pouco relevante

    # Clientes que gastam muito num número reduzido de produtos são premium
    #df['spend_per_distinct_product'] = (
     #   df['total_spend'] / df['lifetime_total_distinct_products'].replace(0, np.nan)
    #)
    #df['spend_per_distinct_product'] = df['spend_per_distinct_product'].fillna(
     #   df['spend_per_distinct_product'].median()
    #)

    # Confirming preprocessing success
    check_nulls(df, FEATURE_COLS)

    return df



def scale_features(df_features: pd.DataFrame):
    """
    Scales the features using RobustScaler, returning both the scaled dataframe and the scaler object for
    flexibility
    """
    df_scaled = df_features.copy()

    scaler = RobustScaler()
    df_scaled[FEATURE_COLS] = scaler.fit_transform(df_features[FEATURE_COLS])

    return df_scaled, scaler



def _check_nulls(df: pd.DataFrame, cols: list):
    """
    Verify if there's nulls in specified columns, to confirm that 
    preprocessing worked as expected
    
    """
    missing = df[cols].isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        raise ValueError(
            f"There's NaN after preprocessing:\n{missing}")