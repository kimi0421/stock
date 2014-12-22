import urlparse
import MySQLdb
import logging
import os
import datetime
import urllib2
import pandas as pd

LEAST_PRICE = 1
LEAST_CAP = 1000000000

class DataCrawler:

    def __init__(self):
        DATABASE_URL = urlparse.urlparse(os.environ['DATABASE_URL'])
        if DATABASE_URL.password is None:
            self.conn = MySQLdb.connect(host=DATABASE_URL.hostname, user=DATABASE_URL.username,
                                        db=DATABASE_URL.path[1:])
        else:
            self.conn = MySQLdb.connect(host=DATABASE_URL.hostname, user=DATABASE_URL.username,
                                        passwd=DATABASE_URL.password, db=DATABASE_URL.path[1:])

        # Setup logger
        self.logger = logging.getLogger('DataCrawler')
        hdlr = logging.FileHandler('logs/data_crawler.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def get_daily_data(self, days=10000, stock_symbols=None, output_dir='output/stock_raw_data/'):
        # Get stock list from database first
        if stock_symbols is None:
            sql = 'SELECT Symbol FROM stock.stock_symbols where LastSale > %s and MarketCap > %s' \
                  % (LEAST_PRICE, LEAST_CAP)
            cur = self.conn.cursor()
            cur.execute(sql)

            self.logger.info("Getting stock list from database")
            stock_symbols = cur.fetchall()
            self.logger.info("Successfully obtained the stock list")

        #Try to get daily data from yahoo hidden api
        # Hidden API url
        import ipdb; ipdb.set_trace()
        url = 'http://ichart.finance.yahoo.com/table.csv?s={symbol}&a={start_month}&b={start_day}&c={start_year}' \
              '&d={end_month}&e={end_day}&f={end_year}&g=d&ignore=.csv'
        end_date = datetime.datetime.utcnow().date()
        start_date = end_date - datetime.timedelta(days)

        for (symbol,) in stock_symbols:
            symbol = symbol.replace('-', '')
            output_file_name = symbol + '.csv'

            if output_file_name in os.listdir(output_dir):
                file_modify_date = pd.to_datetime(os.stat(output_dir + output_file_name)[-1] * 10 ** 9).date()
            else:
                file_modify_date = None

            if end_date == file_modify_date:
                self.logger.info(symbol + " is already downloaded")
            else:
                tmp_url = url.format(symbol=symbol,
                                     start_month=start_date.month, start_day=start_date.day, start_year=start_date.year,
                                     end_month=end_date.month, end_day=end_date.day, end_year=end_date.year)
                try:
                    response = urllib2.urlopen(tmp_url)
                    df = pd.read_csv(response, index_col='Date', parse_dates=True)
                    df = df.sort_index()
                    self.logger.info("Successfully get the data for " + symbol)
                    df.to_csv(output_dir + output_file_name)
                except Exception as e:
                    self.logger.warning(symbol + ' ' + str(e))

        self.logger.info("Successfully finish getting data")



