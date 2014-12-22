from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dashboard.views import DashboardView, StockChartView, TestView, SingleStockView
from forecast_server.views import ForecastGenerateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'stock/', DashboardView.as_view()),
    url(r'^stock_chart/$', StockChartView.as_view()),
    url(r'^stock_api/$', SingleStockView.as_view()),
    url(r'test/', TestView.as_view()),
    url(r'forecast_generate/', ForecastGenerateView.as_view()),

)

urlpatterns += staticfiles_urlpatterns()
