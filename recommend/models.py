from django.db import models

class StockFundamental(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    corp_name = models.CharField(max_length=100)
    market = models.CharField(max_length=10)
    sector = models.CharField(max_length=100, null=True, blank=True)
    stck_prpr = models.IntegerField(null=True, blank=True)  # 현재가
    per = models.FloatField(null=True, blank=True)
    pbr = models.FloatField(null=True, blank=True)
    eps = models.FloatField(null=True, blank=True)
    bps = models.FloatField(null=True, blank=True)

    volatility = models.FloatField(null=True, blank=True)  # 1년 변동성 (%)
    beta = models.FloatField(null=True, blank=True)        # 베타
    market_cap = models.BigIntegerField(null=True, blank=True)  # 시가총액

    def __str__(self):
        return f"{self.corp_name} ({self.ticker})"