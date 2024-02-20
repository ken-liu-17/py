import os
import numpy as np
import pandas as pd

def preprocess(file_path='../data/adj_close_2023.csv'):
    df_price = pd.read_csv(file_path)
    df_price_diff = df_price.diff()
    df_ret = df_price.pct_change*252
    return (df_price, df_ret)        

def buildPortfolio(df_price, df_ret):
    None
    
if __name__ == '__main__':
    print('Building portfolio')
    df_price, df_ret = preprocess()
    