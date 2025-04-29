from django.db import models

class StockFundamental(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    corp_name = models.CharField(max_length=100)
    market = models.CharField(max_length=10)

    stck_prpr = models.IntegerField(null=True, blank=True)
    per = models.FloatField(null=True, blank=True)
    pbr = models.FloatField(null=True, blank=True)
    eps = models.FloatField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.corp_name} ({self.ticker})"