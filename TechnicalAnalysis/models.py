from django.db import models

# Create your models here.


class StockBasicInfo(models.Model):
    Symbol = models.CharField(max_length=30)
    Name = models.TextField()
    Date = models.DateField()
    PrevClose = models.FloatField()
    Open = models.FloatField()
    Close = models.FloatField()
    Low = models.FloatField()
    High = models.FloatField()
    VWAP = models.FloatField()
    Volume = models.FloatField()
    DeliveryPercent = models.FloatField()

    class Meta:
        db_table = "StockBasicInfo"
        unique_together = (("Symbol", "Date"),)


class StockLastUpdate(models.Model):
    StockName = models.TextField()
    StockSymbol = models.CharField(max_length=30, primary_key=True)
    LastUpdateDate = models.DateField(default=None, blank=True)

    class Meta:
        db_table = "StockLastUpdate"


class TechnicalIndicators(models.Model):
    StockName = models.TextField()
    StockSymbol = models.CharField(max_length=30)
    Date = models.DateField()
    SMA25 = models.FloatField()
    SMA50 = models.FloatField()
    RSI = models.FloatField()

    class Meta:
        db_table = "TechnicalIndicators"
        unique_together = (("StockSymbol", "Date"),)
