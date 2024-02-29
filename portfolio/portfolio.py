import os
import numpy as np
import pandas as pd
from alpha import Alpha
from math import floor, sqrt

class Portfolio:
    def __init__(self, cash, alpha):
        self._cash = cash
        self._alpha = alpha
        self._portfolio = pd.DataFrame(dtype=float, columns=self._alpha.df_adj_close.columns, index=self._alpha.df_adj_close.index)
        self._pnL = pd.DataFrame(dtype=float, columns=['pnL'], index=self._alpha.df_adj_close.index)
    
    @property
    def portfolio(self):
    #  shares for each stock
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

    def buildByPrevAdjClose(self):
        self._alpha.df_adj_close_diff.dropna()
        N = len(self._alpha.df_adj_close.columns)
        cash_per_stock = self._cash / N
        for date in self._alpha.df_adj_close_diff.index:
            self._portfolio.loc[date] = self._alpha.df_adj_close.loc[date].apply(lambda x : floor(cash_per_stock / x)) \
                * np.where(self._alpha.df_adj_close_diff.loc[date] >= 0., 1., -1.)
            self._pnL.loc[date] = np.sum(self._portfolio.loc[date] * self._alpha.df_adj_close_diff.loc[date])

    def buildByOpen(self):
        self._alpha.df_adj_close_diff.dropna()
        N = len(self._alpha.df_adj_close.columns)
        cash_per_stock = self._cash / N
        for date in self._alpha.df_open.index:
            self._portfolio.loc[date] = self._alpha.df_open.loc[date].apply(lambda x : floor(cash_per_stock / x)) \
                * np.where(self._alpha.df_adj_close_diff.loc[date] >= 0., 1., -1.)
            self._pnL.loc[date] = np.sum(self._portfolio.loc[date] * (self._alpha.df_adj_close.loc[date] - self._alpha.df_open.loc[date]))

    def sharpeRatio(self):
        self._portfolio_rets = self._pnL.apply(lambda x : x / self._cash)
        mean_ret = self._portfolio_rets.mean()
        print('pnL mean daily return=', self._portfolio_rets.std()['pnL'])
        return sqrt(252.) * mean_ret['pnL'] / self._portfolio_rets.std()['pnL']

    def plot(self):
        pass

if __name__ == '__main__':
    print('Alpha...')
    alpha = Alpha()
    alpha.generate() 
    print('Portfolio...')
    portfolio = Portfolio(float(1e8), alpha)
    print('build by previous adj close ...')
    portfolio.buildByPrevAdjClose()
    print(portfolio.pnL)
    print('sharpe ratio=', portfolio.sharpeRatio())

    print('build by todays open ...')
    portfolio.buildByOpen()
    print(portfolio.pnL)
    print('sharpe ratio=', portfolio.sharpeRatio())