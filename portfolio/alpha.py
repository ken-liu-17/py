import os
import numpy as np
import pandas as pd


class Alpha:
    def __init__(self, df_price):
        self._df_price = df_price
        self._df_price_diff = None
        self._df_ret = None
   
    def __init__(self, adj_close_file_path = '../data/tech_stocks_adj_close_2023.csv', open_file_path = '../data/tech_stocks_open_2023.csv'):
        self._df_adj_close = pd.read_csv(adj_close_file_path, index_col='Date')
        self._df_adj_close_diff = None
        self._df_adj_close_ret = None
        self._df_open = pd.read_csv(open_file_path, index_col='Date')
         
    @property
    def df_adj_close(self):
        return self._df_adj_close

    @property
    def df_adj_close_diff(self):
        return self._df_adj_close_diff
       
    @property
    def df_adj_close_ret(self):
        return self._df_adj_close_ret

    @property
    def df_open(self):
        return self._df_open

    def generate(self):
        self._df_adj_close_diff = self._df_adj_close.diff()
        self._df_adj_close_ret = self._df_adj_close.pct_change() * 252.

if __name__ == '__main__':
    print('alpha ...')
    alpha = Alpha()
    alpha.generate()
    print(alpha.df_ret)