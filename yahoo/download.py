import os
import yfinance as yf
from datetime import datetime
import warnings
import pandas as pd
import numpy as np
import time

##################################################################
# Download Open-High-Low-Close-Volume data from Yahoo finance
#  End-Of-Day and Minute bar data
##################################################################

warnings.simplefilter(action='ignore', category=FutureWarning)

tech_stocks = ['AAPL', 'AMD', 'AMZN', 'BABA', 'BIDU', 'GOOG', 'IBM', 'JD', 'META', 'MSFT', 'NVDA', 'ORCL', 'PDD', 'UBER']
today = datetime.today().strftime('%Y-%m-%d')
EOD_path = '../data/EOD/'
bar_path_prefix = '../data/bar'

def read_sp500_symbols(file_path='../data/SP500_symbols.csv'):
    sp500_df = pd.read_csv(file_path)
    symbols = list(sp500_df['Symbol'])
    return symbols

def create_symbols():
    symbols = read_sp500_symbols()
    symbols_set = set(symbols)
    symbols_set.update(tech_stocks)
    return sorted(symbols_set)

## EOD
def download_single_EOD(symbol, start_date, end_date = None):
#    data = yf.download('AAPL', '2014-01-01', '2024-02-16')
    if end_date is None:
        df = yf.download(symbol, start_date)
    else:
        df = yf.download(symbol, start_date, end_date)
    df.to_csv(EOD_path + symbol+'.csv')
    return df

def download_EOD(symbols, start_date, end_date = None):
    count = 0
    for symbol in symbols:
        download_single_EOD(symbol, start_date, end_date)
        count += 1
        print(str(count) + ' ' + symbol + ' EOD done')
        time.sleep(1)

## minute bar data       
def download_single_bar(symbol, period = '60D', interval = '2m'):
    df = yf.download(tickers=symbol, period = period, interval = interval)
    df.to_csv(bar_path_prefix + '_' + interval + '/' + symbol + '.csv')
    return df

def download_bar(symbols, period = '60D', interval = '2m'):
    count = 0
    for symbol in symbols:
        df = download_single_bar(symbol, period, interval)
        count += 1
        print(str(count) + ' ' + symbol + ' interval=' + interval + ' done')
        time.sleep(1)

# download multiple stocks into 1 dataframe 
def download_EOD_to_one_dataframe(stocks, start_date='2014-01-01'):
    df = yf.download(stocks, start_date)
    df.to_csv('../data/tech_stocks.csv')
    # Adj Close
    df_adj_close = df['Adj Close']
    df_adj_close_2023 = df_adj_close.loc[(df_adj_close.index >= '2023-01-01') & (df_adj_close.index < '2024-01-01')]
    df_adj_close_2023.to_csv('../data/tech/stocks_adj_close_2023.csv')
    # Open
    df_open = df['Open']
    df_open_2023 = df_open.loc[(df_open.index >= '2023-01-01') & (df_open.index < '2024-01-01')]
    df_open_2023.to_csv('../data/tech/stocks_open_2023.csv')
        
    
if __name__ == '__main__':
    print("download...")    
    symbols = create_symbols()
    download_EOD(symbols, '2014-01-01')
    download_bar(symbols, period='7D', interval='1m')
    download_bar(symbols, period='60D', interval='2m')
    download_bar(symbols, period='60D', interval='5m')
    download_bar(symbols, period='60D', interval='15m')
    download_bar(symbols, period='60D', interval='30m')

    #download_EOD_to_one_dataframe(tech_stocks)
