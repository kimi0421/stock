from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from recommendation_server.engine.Recommender import Recommender

# Create your views here.
from dashboard.models import RecommendStocks
from forecast_server.models import Forecast

import logging
import pandas as pd


class RecommendationView(View):

    def __init__(self, **kwargs):
        super(RecommendationView, self).__init__(**kwargs)
        self.logger = logging.getLogger('Recommendation')
        hdlr = logging.FileHandler('logs/recommend.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def get(self, *arg, **kwargs):
        all_forecasted_stock = Forecast.objects.all()
        symbol_index = [stock.symbol for stock in all_forecasted_stock]
        e = [stock.revenue for stock in all_forecasted_stock]
        sigma = [stock.error for stock in all_forecasted_stock]
        df = pd.DataFrame({'e': e, 'sigma': sigma}, index=symbol_index)
        rec = Recommender(df)
        import ipdb; ipdb.set_trace()
        sol = rec.optimize(0.15)
        return HttpResponse('success')

