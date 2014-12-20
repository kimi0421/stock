import os
import multiprocessing
import pandas as pd
from scipy.stats.stats import pearsonr

def corr(df1, df2):
    if len(df1) > len(df2):
        df1 = df1.ix[df2.index]
    else:
        df2 = df2.ix[df1.index]
    return pearsonr(df1, df2)[0]

def find_corr(symbol, stock_df, stock_dir):
    """
    Find correlation with other stocks
    :param symbol:
    :param compare_stock_dir:
    :return:
    """
    compare_stock_files = os.listdir(stock_dir)
    counts = []
    corrs = []
    symbols = []
    for compare_stock_file in compare_stock_files:
        print compare_stock_file
        compare_stock = compare_stock_file.split('.')[0]
        compare_df = pd.read_csv(stock_dir + compare_stock_file, index_col=[0])
        counts.append(len(compare_df))
        corrs.append(corr(stock_df['Adj Close'], compare_df['Adj Close']))
        symbols.append(compare_stock)

    corr_df = pd.DataFrame({'corr': corrs, 'counts': counts}, index=symbols)
    corr_df.to_csv('output/corr/' + symbol + '.csv')

if __name__ == '__main__':
    symbol = 'AAPL'
    stock_df = pd.read_csv('data_crawler/stock_raw_data/AAPL.csv', index_col=[0])
    find_corr(symbol, stock_df, 'data_crawler/stock_raw_data/')

