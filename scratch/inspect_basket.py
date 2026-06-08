import pandas as pd

df_basket = pd.read_csv("data/customer_basket.csv", nrows=5)
print("Basket columns:", df_basket.columns.tolist())
print(df_basket.head())
