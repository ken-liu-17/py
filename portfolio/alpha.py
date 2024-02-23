import os
import numpy as np
import pandas as pd


class Alpha:
    def __init__(self, df_price):
        self._df_price = df_price
        self._df_price_diff = None
        self._df_ret = None
   
    def __init__(self, file_path):
        self._df_price = pd.read_csv(file_path, index_col='Date')
        self._df_price_diff = None
        self._df_ret = None
         
    @property
    def df_price(self):
        return self._df_price

    @property
    def df_price_diff(self):
        return self._df_price_diff
       
    @property
    def df_ret(self):
        return self._df_ret

    def generate(self):
        self._df_price_diff = self._df_price.diff()
        self._df_ret = self._df_price.pct_change() * 252.
    

if __name__ == '__main__':
    print('alpha ...')
    alpha = Alpha('../data/adj_close_2023.csv')
    alpha.generate()
    print(alpha.df_ret)