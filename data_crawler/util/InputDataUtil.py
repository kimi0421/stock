import os
import urlparse
import MySQLdb
import pandas as pd
import pandas.rpy.common as com
import rpy2.robjects as robjects


class InputUtil:

    def __init__(self):
        DATABASE_URL = urlparse.urlparse(os.environ['DATABASE_URL'])
        if DATABASE_URL.password is None:
            self.conn = MySQLdb.connect(host=DATABASE_URL.hostname, user=DATABASE_URL.username,
                                        db=DATABASE_URL.path[1:])
        else:
            self.conn = MySQLdb.connect(host=DATABASE_URL.hostname, user=DATABASE_URL.username,
                                        passwd=DATABASE_URL.password, db=DATABASE_URL.path[1:])

    @staticmethod
    def get_stock_symbols_list():
        robjects.r('require(TTR)')
        stock_symbols = robjects.r('TTR::stockSymbols()')
        stock_symbols_df = com.convert_robj(stock_symbols)
        return stock_symbols_df[~pd.isnull(stock_symbols_df['Symbol'])]

    def update_stock_list_database(self):
        stock_df = self.get_stock_symbols_list()

        #Change the column name
        stock_df = stock_df[['Symbol', 'Name', 'IPOyear', 'Sector', 'LastSale', 'MarketCap']]

        #Update the database
        stock_df.to_sql('stock_symbols', self.conn, if_exists='replace', index=True)

