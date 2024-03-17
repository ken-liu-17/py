import os
import yfinance as yf
from datetime import datetime
import warnings
import pandas as pd
import numpy as np
import time
import pathlib
from download import Download

#############################################################################
# Download Open-High-Low-Close-Volume data from Yahoo finance End-Of-Day
#   start_date is inclusive
#   end_date is exclusive
#############################################################################

warnings.simplefilter(action='ignore', category=FutureWarning)

class DownloadEod(Download):
    def __init__(self, start_date, end_date, symbols=None, data_dir_base=None):
        Download.__init__(self, start_date, end_date, symbols, data_dir_base)
        self._eod_path = None

    @property
    def eod_path(self):
        return self.data_dir_base + '/EOD'
   
    @property
    def total_path(self):
        return self.eod_path + '/' + self.start_to_end_date_path
     
    def __download_single(self, symbol):
        #    data = yf.download('AAPL', '2014-01-01', '2024-02-16')
        df = yf.download(symbol, self.start_date, self.end_date)  
        df.to_csv(self.total_path + '/' + symbol + '.csv')
        return df

    def download(self):
        Download.make_path(self.total_path)
        count = 0
        for symbol in self.symbols:
            self.__download_single(symbol)
            count += 1
            print(str(count) + ' ' + symbol + ' EOD done')
            time.sleep(1)

# download multiple stocks into 1 dataframe 
#def download_EOD_to_one_dataframe(stocks, start_date='2014-01-01'):
#    df = yf.download(stocks, start_date)
#    df.to_csv('../data/tech_stocks.csv')
#    # Adj Close
#    df_adj_close = df['Adj Close']
#    df_adj_close_2023 = df_adj_close.loc[(df_adj_close.index >= '2023-01-01') & (df_adj_close.index < '2024-01-01')]
#    df_adj_close_2023.to_csv('../data/tech/stocks_adj_close_2023.csv')
#    # Open
#    df_open = df['Open']
#    df_open_2023 = df_open.loc[(df_open.index >= '2023-01-01') & (df_open.index < '2024-01-01')]
#    df_open_2023.to_csv('../data/tech/stocks_open_2023.csv')


if __name__ == '__main__':
    print("download EOD...")    
    start_date = '2024-03-11'
    end_date = '2024-03-16'
    download_eod = DownloadEod(start_date=start_date, end_date=end_date)
    download_eod.download()
    #download_EOD_to_one_dataframe(tech_stocks)
