from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from recommendation_server.engine.Recommender import Recommender

# Create your views here.
from dashboard.models import RecommendStocks
from forecast_server.models import Forecast

import logging
import json
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
        # Test
        df['e'] -= 0.8 * df['sigma']

        # First Time
        rec = Recommender(df, 760)
        sol = rec.optimize(0.03)
        sol_df = pd.DataFrame({'weight': list(sol['x'])}, index=df.index)
        sol_df = sol_df.sort('weight')[-200:]

        # Second Time
        df = df.ix[sol_df.index]
        rec = Recommender(df, 760)
        sol = rec.optimize(0.03)
        sol_df = pd.DataFrame({'weight': list(sol['x'])}, index=df.index)
        sol_df = sol_df.sort('weight')[-60:]

        # Third Time
        df = df.ix[sol_df.index]
        rec = Recommender(df, 760)
        sol = rec.optimize(0.03)
        sol_df = pd.DataFrame({'weight': list(sol['x'])}, index=df.index)
        sol_df = sol_df.sort('weight')[-6:]

        df = df.ix[sol_df.index]
        rec = Recommender(df, 760)
        sol = rec.optimize(0.03)
        sol_df = pd.DataFrame({'weight': list(sol['x'])}, index=df.index)
        return HttpResponse(json.dumps(sol_df.index.tolist()))

