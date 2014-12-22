import os
import pandas as pd
from scipy.stats.stats import pearsonr

def corr(df1, df2):
    if len(df1) > len(df2):
        df1 = df1.ix[df2.index]
    else:
        df2 = df2.ix[df1.index]
    # Dropna
    df1 = df1.dropna()
    df2 = df2.dropna()
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
    print "Processing ", symbol
    for compare_stock_file in compare_stock_files:
        compare_stock = compare_stock_file.split('.')[0]
        compare_df = pd.read_csv(stock_dir + compare_stock_file, index_col=[0])
        counts.append(len(compare_df))
        corrs.append(corr(stock_df['Adj Close'], compare_df['Adj Close']))
        symbols.append(compare_stock)

    corr_df = pd.DataFrame({'corr': corrs, 'counts': counts}, index=symbols)
    corr_df.to_csv('output/corr/' + symbol + '.csv')

def generate_corr_table():
    stock_files = os.listdir('output/corr/')
    stock_index = []
    pos = []
    neg = []
    for stock_file in stock_files:
        symbol = stock_file.split('.')[0]
        try:
            print symbol
            df = pd.read_csv('output/corr/' + stock_file, index_col=[0])
            df = df.drop(symbol)
            sorted_df = df.sort('corr').dropna()
            sorted_df = sorted_df[sorted_df['counts'] > 365 * 2]
            stock_index.append(symbol)
            pos.append(sorted_df.index[-1])
            neg.append(sorted_df.index[0])
        except:
            import ipdb; ipdb.set_trace()
            df = pd.read_csv('output/corr/' + stock_file, index_col=[0])
            count = df.loc[symbol, 'counts']
            sorted_df = df.sort('corr').dropna()
            sorted_df = sorted_df[sorted_df['counts'] > count]

    df = pd.DataFrame({'pos': pos, 'neg': neg, 'symbol': stock_index})
    df.to_csv('output/corr_table/corr.csv')
    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    # jobs = []
    # stock_dir = 'output/stock_raw_data/'
    # all_files = os.listdir(stock_dir)
    # for stock_file in all_files[2000:]:
    #     if stock_file in os.listdir('output/corr/'):
    #         pass
    #     symbol = stock_file.split('.')[0]
    #     stock_df = pd.read_csv(stock_dir + stock_file, index_col=[0])
    #     find_corr(symbol, stock_df, stock_dir)
    generate_corr_table()