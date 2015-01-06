from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from forecast_server.models import StockToForecast, Forecast
from forecast_server.engine.ForecastModels import SVRModel
from forecast_server.engine.Forecaster import Forecaster

import logging
import pandas as pd
import numpy as np
# Create your views here.
class ForecastGenerateView(View):

    def __init__(self, **kwargs):
        super(ForecastGenerateView, self).__init__(**kwargs)
        self.logger = logging.getLogger('ForecastGenerateView')
        hdlr = logging.FileHandler('logs/forecast_generate.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def get_data(symbol, n):
        df = pd.read_csv('output/stock_raw_data/' + symbol + '.csv', index_col=[0])
        return df[-n:]

    def get(self, *arg, **kwargs):
        import ipdb; ipdb.set_trace()
        ml_model = SVRModel()
        stocks_to_forecast = StockToForecast.objects.all()
        id = 0
        for stock in stocks_to_forecast:
            symbol = stock.symbol
            symbol_pos = stock.pos
            symbol_neg = stock.neg

            try:
                self.logger.info("Processing stock %s." % symbol)
                stock_df = self.get_data(symbol, 365 * 2)
                stock_df_pos = self.get_data(symbol_pos, 365 * 2)
                stock_df_neg = self.get_data(symbol_neg, 365 * 2)
                fcster = Forecaster(stock_df, stock_df_pos, stock_df_neg, ml_model)
                fcst_result = fcster.forecast(5)
                forecast_entry = Forecast(id=id, symbol=symbol, revenue=fcst_result['return'],
                                          error=np.sum(fcst_result['error']))
                forecast_entry.save()
                id += 1
                self.logger.info("Successfully processing stock %s." % symbol)
            except Exception as e:
                self.logger.warning(str(e) + ' ' + symbol)
        return HttpResponse('Success!')


