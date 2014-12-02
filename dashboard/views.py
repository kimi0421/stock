from django.shortcuts import render
from django.views.generic.base import View, TemplateView
# Create your views here.


class DashboardView(TemplateView):

    template_name = 'index.html'
