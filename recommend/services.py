import random
from recommend.models import StockFundamental

def recommend_stocks_by_profile(profile_type):
    qs = StockFundamental.objects.exclude(volatility__isnull=True).exclude(beta__isnull=True)

    # 시가총액 기준 상위/하위 퍼센트 커팅 로직은 추가 가능
    if profile_type == "공격투자형":
        qs = qs.filter(
            volatility__gt=30,
            beta__gt=1.5
        )
        # qs = qs.filter(market_cap__lte=하위_50퍼센트값)

    elif profile_type == "적극투자형":
        qs = qs.filter(
            volatility__gte=20, volatility__lte=30,
            beta__lte=1.5,
            market='KOSDAQ'
        )

    elif profile_type == "위험중립형":
        qs = qs.filter(
            volatility__gte=15, volatility__lte=25,
            beta__lte=1.2
        )

    elif profile_type == "안정추구형":
        qs = qs.filter(
            volatility__gte=10, volatility__lte=18,
            beta__lte=1.0,
            # market_cap__gte=상위_100위_시가총액
        )

    elif profile_type == "안정형":
        qs = qs.filter(
            volatility__lte=12,
            beta__lte=0.8,
            # market_cap__gte=상위_50위_시가총액
        )

    else:
        return []

    stocks = list(qs)

    return stocks