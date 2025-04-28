from django.shortcuts import render
from .utils.api import get_stock_news, get_market_indices, get_top_movers

def index(request):
    market_input = request.GET.get("market", "")  # ""이면 전체
    valid_codes = ["", "0001", "1001", "2001"]

    # 유효하지 않은 값이 들어오면 전체로 처리
    if market_input not in valid_codes:
        market_input = ""

    # 급등/급락 종목 가져오기
    top_rising = get_top_movers(market=market_input, is_rising=0, top_n=5)
    top_falling = get_top_movers(market=market_input, is_rising=1, top_n=5)

    # 시장 지수 및 뉴스
    market_data = get_market_indices()
    stock_news = get_stock_news()

    context = {
        "market_data": market_data,
        "stock_news": stock_news,
        "top_rising": top_rising,
        "top_falling": top_falling,
        "selected_market": market_input  # 현재 선택된 시장
    }
    return render(request, 'dashboard/index.html', context)