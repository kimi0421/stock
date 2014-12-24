# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class StockToForecast(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    symbol = models.CharField(max_length=11)
    pos = models.CharField(max_length=11)
    neg = models.CharField(max_length=11)

    class Meta:
        db_table = 'stock_to_forecast'


class Forecast(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    symbol = models.CharField(max_length=11)
    revenue = models.FloatField(max_length=11)
    error = models.FloatField(max_length=11)

    class Meta:
        db_table = 'forecast'
