import os
import numpy as np
import pandas as pd
from alpha import Alpha
from math import floor, sqrt

class Portfolio:
    def __init__(self, cash, alpha):
        self._cash = cash
        self._alpha = alpha
        self._portfolio = pd.DataFrame(dtype=float, columns=self._alpha.df_price.columns, index=self._alpha.df_price.index)
        self._pnL = pd.DataFrame(dtype=float, columns=['pnL'], index=self._alpha.df_price.index)
    
    @property
    def portfolio(self):
        return self._portfolio
       
    @property
    def alpha(self):
        return self._alpha
        
    @property
    def portfolio(self):
        return self._portfolio

    @property
    def pnL(self):
        return self._pnL

    def build(self):
        df_price = self._alpha.df_price
        df_price_diff = self._alpha.df_price_diff
        #df_price_ret = self._alpha.df_ret
        N = len(df_price.columns)
        cash_per_stock = self._cash / N
        for date in df_price_diff.index:
            diffs = df_price_diff.loc[date]
            diffs = np.where(diffs.isna(), 0, diffs)
            diffs = np.where(diffs > 0., 1., diffs)
            diffs = np.where(diffs < 0., -1., diffs)
            self._portfolio.loc[date] = df_price.loc[date].apply(lambda x : floor(cash_per_stock / x)) * diffs
            self._pnL.loc[date] = np.sum(self._portfolio.loc[date] * df_price_diff.loc[date])

    def sharpeRatio(self):
        self._portfolio_rets = self._pnL.apply(lambda x : x / self._cash)
        mean_ret = self._portfolio_rets.mean()
        print(mean_ret)
        print(mean_ret, self._portfolio_rets.std()['pnL'])
        return sqrt(252.) * mean_ret['pnL'] / self._portfolio_rets.std()['pnL']

    def plot(self):
        pass

if __name__ == '__main__':
    print('Alpha...')
    alpha = Alpha('../data/adj_close_2023.csv')
    alpha.generate() 
    print('Portfolio...')
    portfolio = Portfolio(float(1e8), alpha)
    portfolio.build()
    print('sharpe ratio=', portfolio.sharpeRatio())