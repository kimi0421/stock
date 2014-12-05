import urllib2
import logging
import datetime
import json
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View
# Create your views here.
from dashboard.models import RecommendStocks

logger = logging.getLogger(__name__)


class DashboardView(TemplateView):

    template_name = 'index.html'

    @staticmethod
    def get_changes(stock_symobls):
        url = 'http://finance.yahoo.com/d/quotes.csv?s={symbols}&f=snw1'
        symbols_str = '+'.join(stock_symobls)
        response = urllib2.urlopen(url.format(symbols=symbols_str))
        df = pd.read_csv(response, names=['symbol', 'name', 'change'])
        # Return the list of changes
        try:
            changes = [change.split(' ')[-1] for change in df['change']]
            return changes
        except Exception as e:
            logger.debug("Something wrong with Yahoo API for getting the change")
            logger.error(e)

    def get_context_data(self, **kwargs):
        #box_colors = ['bg-red', 'bg-yellow', 'bg-aqua', 'bg-green', 'bg-lime', 'bg-maroon']
        recommended_stocks = RecommendStocks.objects.filter(sector='Technology')
        recommended_stock_symbols = [stock.symbol for stock in recommended_stocks]
        recommended_stock_changes = self.get_changes(recommended_stock_symbols)

        # Create context return to html
        context = {'stocks': {}}
        for idx, stock in enumerate(recommended_stock_symbols):

            # Check whether it is positive or negative
            if recommended_stock_changes[idx][0] == '+':
                box_color = 'bg-green'
            else:
                box_color = 'bg-red'

            context['stocks'][stock]= {'change': recommended_stock_changes[idx][:-1],
                                       'box_color': box_color}
        return context


class StockChartView(View):

    @staticmethod
    def get_daily_stock_data(symbol, start_date, end_date):
        """
        This method is used to get stock data and convert to dictionary
        :param symbol: stock symbol
        :return: dict format
        """
        stock_url = 'http://ichart.finance.yahoo.com/table.csv?s={symbol}&a={start_month}&b={start_day}&c={start_year}' \
                    '&d={end_month}&e={end_day}&f={end_year}&g=d&ignore=.csv'
        formatted_url = stock_url.format(symbol=symbol,
                                         end_month=end_date.month - 1, end_day=end_date.day, end_year=end_date.year,
                                         start_month=start_date.month - 1, start_day=start_date.day, start_year=start_date.year)
        stock_df = pd.read_csv(urllib2.urlopen(formatted_url), index_col=['Date'], parse_dates=True)
        stock_df = stock_df.sort_index()
        stock_data = [{'x': idx.value // 10 ** 6, 'y': stock_df.ix[idx]['Adj Close']} for idx in stock_df.index]
        return stock_data

    def get(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return: Stock data json for recommended stocks
        """
        if request.method == 'GET':

            # Chart color
            chart_colors = ["#86B5D4", "#979799", "#BAD748", "#F5E1C8", "#EF8832", "#CAC5AA"]
            chart_type_dict = {'1y': 365, '3m': 91, '1m': 31, '5d': 5, '1d': 1}

            # sector type such as: All, Technology
            sector = request.GET.get('sector')
            # Four chart_type: 1y, 3m, 1m, 5d, 1d
            chart_type = request.GET.get('chart_type')
            chart_duration = chart_type_dict[chart_type]

            recommended_stocks = RecommendStocks.objects.filter(sector=sector)
            recommended_stock_symbols = [stock.symbol for stock in recommended_stocks]

            # Set up end_date and start_date
            end_date = pd.to_datetime(datetime.date.today())
            start_date = end_date - datetime.timedelta(chart_duration)

            response = []
            if chart_duration > 5:
                for i, symbol in enumerate(recommended_stock_symbols):
                    chart_data = self.get_daily_stock_data(symbol, start_date, end_date)
                    chart_color = chart_colors[i]
                    response.append({'key': symbol, 'values': chart_data, 'color': chart_color})

            return HttpResponse(json.dumps(response), content_type="application/json")




