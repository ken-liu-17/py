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

def download_stocks_to_one_dataframe(stocks, start_date='2014-01-01'):
    df = yf.download(stocks, start_date)
    df.to_csv('../data/tech_stocks.csv')
    # Adj Close
    df_adj_close = df['Adj Close']
    df_adj_close_2023 = df_adj_close.loc[(df_adj_close.index >= '2023-01-01') & (df_adj_close.index < '2024-01-01')]
    df_adj_close_2023.to_csv('../data/tech_stocks_adj_close_2023.csv')
    # Open
    df_open = df['Open']
    df_open_2023 = df_open.loc[(df_open.index >= '2023-01-01') & (df_open.index < '2024-01-01')]
    df_open_2023.to_csv('../data/tech_stocks_open_2023.csv')
        
    
if __name__ == '__main__':
    print("download...")    
    #symbols = read_sp500_symbols()
    #download_quotes(symbols, '2014-01-01')
    tech_stocks = ['AAPL', 'AMD', 'AMZN', 'BABA', 'BIDU', 'GOOG', 'IBM', 'JD', 'META', 'MSFT', 'NVDA', 'ORCL', 'PDD', 'UBER']
    download_stocks_to_one_dataframe(tech_stocks)

