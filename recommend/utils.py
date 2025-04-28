from recommend.models import StockFundamental
import random

def recommend_stocks_by_profile(profile_type, count=10):
    qs = StockFundamental.objects.all()

    if profile_type == "공격투자형":
        qs = qs.filter(per__gte=10, per__lte=50, pbr__gte=1.0, eps__gte=0)
    elif profile_type == "적극투자형":
        qs = qs.filter(per__gte=5, per__lte=20, pbr__gte=1.0, pbr__lte=3.0, eps__gte=0)
    elif profile_type == "위험중립형":
        qs = qs.filter(per__gte=5, per__lte=15, pbr__gte=0.5, pbr__lte=2.5, eps__gte=0)
    elif profile_type == "안정추구형":
        qs = qs.filter(per__gte=5, per__lte=10, pbr__gte=0.5, pbr__lte=1.5, eps__gte=0)
    elif profile_type == "안정형":
        qs = qs.filter(per__lte=5, pbr__lte=1.0, eps__gte=0)
    else:
        return []  # 잘못된 타입

    stocks = list(qs)

    if len(stocks) > count:
        stocks = random.sample(stocks, count)

    return stocks
