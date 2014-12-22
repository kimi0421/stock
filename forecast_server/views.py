from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from forecast_server.models import StockToForecast

from forecast_server.engine.ForecastModels import SVRModel
from forecast_server.engine.Forecaster import Forecaster

import pandas as pd
# Create your views here.
class ForecastGenerateView(View):

    @staticmethod
    def get_data(symbol, n):
        df = pd.read_csv('output/stock_raw_data/' + symbol + '.csv', index_col=[0])
        return df[-n:]

    def get(self, *arg, **kwargs):
        ml_model = SVRModel()
        stocks_to_forecast = StockToForecast.objects.all()
        for stock in stocks_to_forecast:
            import ipdb; ipdb.set_trace()
            symbol = stock.symbol
            symbol_pos = stock.pos
            symbol_neg = stock.neg

            stock_df = self.get_data(symbol, 365 * 2)
            stock_df_pos = self.get_data(symbol_pos, 365 * 2)
            stock_df_neg = self.get_data(symbol_neg, 365 * 2)
            fcster = Forecaster(stock_df, stock_df_pos, stock_df_neg, ml_model)
            fcster.forecast(5)
        return True


