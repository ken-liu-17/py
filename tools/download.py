import os
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import pandas as pd
import numpy as np
import time
import pathlib

##################################################################
# Download Open-High-Low-Close-Volume data from Yahoo finance
# This is base class
##################################################################
warnings.simplefilter(action='ignore', category=FutureWarning)

tech_stocks = ['AAPL', 'AMD', 'AMZN', 'BABA', 'BIDU', 'GOOG', 'IBM', 'JD', 'META', 'MSFT', 'NVDA', 'ORCL', 'PDD', 'UBER']
date_format = '%Y-%m-%d'
today = datetime.today().strftime(date_format)
today_plus_1 = (datetime.today()+timedelta(1)).strftime('%Y-%m-%d')
YAHOO_DATA_DIR = os.getenv('YAHOO_DATA')


class Download:
    def __init__(self, start_date=today, end_date=today_plus_1, symbols=None, data_dir_base=None):
        self._start_date = start_date
        self._end_date = end_date
        if data_dir_base is None:
            self._data_dir_base = YAHOO_DATA_DIR
        else:
            self._data_dir_base = data_dir_base
        if symbols is None:
            self._symbols = Download.__createSymbols()
        else:
            self._symbols = symbols
    
    @property
    def symbols(self):
        return self._symbols

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def end_date_plus_1(self):
        date = datetime.strptime(self.end_date, date_format).date()
        return (date + timedelta(1)).strftime(date_format)
    
    @property
    def start_to_end_date_path(self):
        start_str = self.start_date.replace('-', '')
        end_str = self.end_date.replace('-', '')
        return start_str + '-' + end_str
    
    @property
    def data_dir_base(self):
        return self._data_dir_base
   
    @staticmethod 
    def __createSymbols():
        symbols = Download.read_sp500_symbols()
        symbols_set = set(symbols)
        symbols_set.update(tech_stocks)
        return sorted(symbols_set)
    
    @staticmethod  
    def read_sp500_symbols(file_path=YAHOO_DATA_DIR + '/SP500_symbols.csv'):
        sp500_df = pd.read_csv(file_path)
        symbols = list(sp500_df['Symbol'])
        return symbols
    
    @staticmethod
    def make_path(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print('today=', today, 'today+1=', today_plus_1)
    print("download: ")    
    download = Download()
    print(download.start_date) 
    print(download.end_date) 
    print(download.end_date_plus_1) 
    print(download.data_dir_base) 
    print(download.symbols) 
