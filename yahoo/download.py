import os
import yfinance as yf
from datetime import datetime
import warnings
import pandas as pd
import numpy as np

##################################################################
# Download Open-High-Low-Close-Volume data from Yahoo finance
##################################################################

warnings.simplefilter(action='ignore', category=FutureWarning)

today = datetime.today().strftime('%Y-%m-%d')
csv_path = '../data/yahoo/'

def download_one(symbol, start_date, end_date = None):
#    data = yf.download('AAPL', '2014-01-01', '2024-02-16')
    if end_date is None:
        df = yf.download(symbol, start_date)
    else:
        df = yf.download(symbol, start_date, end_date)
    df.to_csv(csv_path+symbol+'.csv')
    return df

def download_quotes(symbols, start_date, end_date = None):
    count = 0
    for symbol in symbols:
        download_one(symbol, start_date, end_date)
        count += 1
        print(symbol + ' done ' + str(count))
        
def read_sp500_symbols(file_path='../data/SP500_symbols.csv'):
    sp500_df = pd.read_csv(file_path)
    symbols = list(sp500_df['Symbol'])
    return symbols

if __name__ == '__main__':
    print("download...")    
    symbols = read_sp500_symbols()
    download_quotes(symbols, '2014-01-01')
