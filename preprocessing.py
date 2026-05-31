import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler





SPEND_COLS = [
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
]


# Estas são as colunas que entram no modelo 

FEATURE_COLS = [
    #  Demográficas 
    'age',
    'is_female',
    'household_size',
    'edu_Bsc',
    'edu_Msc',
    'edu_Phd',
    # Comportamento de compra 
    'has_loyalty_card',
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',
    # Valor total 
    'total_spend',
    'spend_per_distinct_product',
    # Shares de categoria

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
]




def build_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe o DataFrame bruto de customer_info.csv e devolve
    um DataFrame com todas as features de negócio criadas.

    Não faz escalonamento — isso é feito à parte em scale_features().
    Preserva customer_id para join posterior.

    Parameters
    ----------
    df_raw : pd.DataFrame
        DataFrame lido diretamente do CSV, sem transformações.

    Returns
    -------
    pd.DataFrame
        DataFrame com as features originais + features novas.
        Pronto para scale_features().
    """
    df = df_raw.copy()

    
    # Limpeza de colunas que já existem
    

    #  NaN significa "nenhuma reclamação registada"
    df['number_complaints'] = df['number_complaints'].fillna(0)

    #  loyalty_card_number — só existe o valor 1.0 (tem cartão)
    df['has_loyalty_card'] = df['loyalty_card_number'].notna().astype(int)
    

    #  year_first_transaction — existem valores futuros (2026-2029)
    df['year_first_transaction'] = df['year_first_transaction'].clip(upper=REFERENCE_YEAR)

    #  NaN é 0 (assumimos que nao existe filhos/teens)
    df['kids_home'] = df['kids_home'].fillna(0)
    df['teens_home'] = df['teens_home'].fillna(0)

    #  Nos proximos três NaN substituimos pela mediana
    df['distinct_stores_visited'] = df['distinct_stores_visited'].fillna(
        df['distinct_stores_visited'].median()
    )

    
    df['typical_hour'] = df['typical_hour'].fillna(df['typical_hour'].median())

    
    df['percentage_of_products_bought_promotion'] = df['percentage_of_products_bought_promotion'].fillna(
        df['percentage_of_products_bought_promotion'].median()
    )

    # Colunas de gasto com NaN é 0
    for col in SPEND_COLS:
        df[col] = df[col].fillna(0)

    

    #  Idade 
    df['customer_birthdate'] = pd.to_datetime(
        df['customer_birthdate'],
        format='%m/%d/%Y %I:%M %p',
        errors='coerce'  # datas inválidas ficam NaT
    )
    df['age'] = REFERENCE_YEAR - df['customer_birthdate'].dt.year
    df['age'] = df['age'].fillna(df['age'].median())  # NaT → mediana
    df = df.drop(columns=['customer_birthdate'])

    # Género, 1 = feminino, 0 = masculino
    df['is_female'] = (df['customer_gender'] == 'female').astype(int)

    # Grau académico, Bsc. / Msc. / Phd. / No_Degree
    df['education_level'] = (
        df['customer_name']
        .str.extract(r'^(Bsc|Msc|Phd)\.', expand=False)
        .fillna('No_Degree')
    )
    
    edu_dummies = pd.get_dummies(
        df['education_level'],
        prefix='edu',
        drop_first=False,
        dtype=int
    )
    df = pd.concat([df, edu_dummies], axis=1)

    

    # numero de pessoas em casa
    df['household_size'] = df['kids_home'] + df['teens_home']

    # há quantos anos é cliente
    df['customer_tenure'] = REFERENCE_YEAR - df['year_first_transaction']
    df['customer_tenure'] = df['customer_tenure'].fillna(df['customer_tenure'].median())

    


    df['total_spend'] = df[SPEND_COLS].sum(axis=1)

    # percentagem de cada categoria no total
    
    for col in SPEND_COLS:
        share_name = 'share_' + col.replace('lifetime_spend_', '')
        df[share_name] = df[col] / df['total_spend'].replace(0, np.nan)
        df[share_name] = df[share_name].fillna(0)

    # Clientes que gastam muito num número reduzido de produtos são premium
    df['spend_per_distinct_product'] = (
        df['total_spend'] / df['lifetime_total_distinct_products'].replace(0, np.nan)
    )
    df['spend_per_distinct_product'] = df['spend_per_distinct_product'].fillna(
        df['spend_per_distinct_product'].median()
    )

    
    # garantir que não há NaN nas feature cols
    
    _check_no_nulls(df, FEATURE_COLS)

    return df




def scale_features(df_features: pd.DataFrame) -> tuple[pd.DataFrame, RobustScaler]:
    """

    Parameters
    
    df_features : pd.DataFrame
        Output de build_features(). Deve conter todas as colunas de FEATURE_COLS.

    Returns
    
    df_scaled : pd.DataFrame
        DataFrame com as mesmas colunas, mas valores escalados em FEATURE_COLS.
    scaler : RobustScaler
        O scaler fitado (útil para inverse_transform no profiling).
    """
    df_scaled = df_features.copy()

    scaler = RobustScaler()
    df_scaled[FEATURE_COLS] = scaler.fit_transform(df_features[FEATURE_COLS])

    return df_scaled, scaler



# verificação de NaN


def _check_no_nulls(df: pd.DataFrame, cols: list) -> None:
    """
    Verificar se existem NaN nas colunas especificadas.
    
    """
    missing = df[cols].isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        raise ValueError(
            f"Existem NaN nas features após o preprocessing:\n{missing}\n"
            "Revê a lógica de imputação em build_features()."
        )