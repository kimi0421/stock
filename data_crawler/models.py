from django.db import models

# Create your models here.
class StockSymbols(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    symbol = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    year = models.CharField(max_length=45, blank=True)
    sector = models.CharField(max_length=45, blank=True)

    class Meta:
        managed = False
        db_table = 'stock_symbols'
