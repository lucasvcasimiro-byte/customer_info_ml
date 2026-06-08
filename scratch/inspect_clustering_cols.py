import pandas as pd
df = pd.read_csv("data/ci_clustering.csv", nrows=5)
print("ci_clustering columns:", df.columns.tolist())
