import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns
import math
import os
from sklearn.preprocessing import RobustScaler


def load_raw_data(info_path: str = "data/customer_info.csv",
                  basket_path: str = "data/customer_basket.csv"):
    # Get the project root (parent of functions directory), for folder organization
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    info_path = os.path.join(project_root, info_path)
    basket_path = os.path.join(project_root, basket_path)
    
    df_info   = pd.read_csv(info_path)
    df_basket = pd.read_csv(basket_path)
    return df_info, df_basket