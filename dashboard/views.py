from django.shortcuts import render
from .utils import get_stock_news, get_market_indices, get_top_movers

def index(request):
    market_data = get_market_indices()  # 주요 지수 데이터 가져오기
    stock_news = get_stock_news()  # 네이버 주식 뉴스 가져오기
    top_risers = get_top_movers(market="J", is_rising=0, top_n=5)  # 코스피 급등 TOP 5
    top_fallers = get_top_movers(market="J", is_rising=1, top_n=5)  # 코스피 급락 TOP 5

    # 🔥 상승/하락 여부를 판단하는 새로운 키 추가
    for market in market_data:
        if market["price_change"].startswith("▲"):
            market["trend"] = "up"  # 상승
        elif market["price_change"].startswith("▼"):
            market["trend"] = "down"  # 하락
        else:
            market["trend"] = "neutral"  # 변동 없음

    context = {
        "market_data": market_data,
        "stock_news": stock_news
    }
    return render(request, 'dashboard/index.html', context)