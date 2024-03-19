import os
import yfinance as yf
from datetime import datetime
import warnings
import pandas as pd
import numpy as np
import time
from download import Download

##################################################################
# Download Open-High-Low-Close-Volume data from Yahoo finance
#   minute bar data
#   start_date is inclusive
#   end_date is exclusive
##################################################################
warnings.simplefilter(action='ignore', category=FutureWarning)

bar_path_prefix = '../data/bar'


class DownloadBar(Download):
    def __init__(self, start_date, end_date, interval='1m', symbols=None, data_dir_base=None):
        Download.__init__(self, start_date, end_date, symbols, data_dir_base)
        self._interval = interval
        self._bar_path = None
        
    @property
    def interval(self):
        return self._interval
    
    @property
    def bar_path(self):
        return self.data_dir_base + '/bar_' + self.interval
   
    @property
    def total_path(self):
        return self.bar_path + '/' + self.start_to_end_date_path
     
    def __download_single(self, symbol):
        df = yf.download(tickers=symbol, start = self.start_date, end = self.end_date, interval = self.interval)
        df.to_csv(self.total_path + '/' + symbol + '.csv')
        return df

    def download(self):
        Download.make_path(self.total_path)
        count = 0
        for symbol in self.symbols:
            self.__download_single(symbol)
            count += 1
            print(str(count) + ' ' + symbol + ' interval=' + self.interval + ' done')
            time.sleep(1)


if __name__ == '__main__':
    print("download bar data ...")
    start_date = '2024-03-11'
    end_date = '2024-03-16'
    #1m
    download_bar_1m = DownloadBar(start_date=start_date, end_date=end_date, interval='1m')
    download_bar_1m.download()
    #2m
    download_bar_2m = DownloadBar(start_date=start_date, end_date=end_date, interval='2m')
    download_bar_2m.download()
    #5m
    download_bar_5m = DownloadBar(start_date=start_date, end_date=end_date, interval='5m')
    download_bar_5m.download()
    #15m
    download_bar_15m = DownloadBar(start_date=start_date, end_date=end_date, interval='15m')
    download_bar_15m.download()
    #30m
    download_bar_30m = DownloadBar(start_date=start_date, end_date=end_date, interval='30m')
    download_bar_30m.download()