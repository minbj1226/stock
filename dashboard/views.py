from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .utils.api import get_stock_news, get_market_indices, get_top_movers

def index(request):
    market_input = request.GET.get("market", "")  # ""이면 전체
    valid_codes = ["", "0001", "1001", "2001"]
    if market_input not in valid_codes:
        market_input = ""

    top_rising = get_top_movers(market=market_input, is_rising=0, top_n=5)
    top_falling = get_top_movers(market=market_input, is_rising=1, top_n=5)
    market_data = get_market_indices()
    stock_news = get_stock_news()

    context = {
        "market_data": market_data,
        "stock_news": stock_news,
        "top_rising": top_rising,
        "top_falling": top_falling,
        "selected_market": market_input
    }
    return render(request, 'dashboard/index.html', context)


# ✅ 추가: 비동기 탭 요청 처리
def ajax_market_stocks(request):
    market_input = request.GET.get("market", "")
    valid_codes = ["", "0001", "1001", "2001"]
    if market_input not in valid_codes:
        market_input = ""

    top_rising = get_top_movers(market=market_input, is_rising=0, top_n=5)
    top_falling = get_top_movers(market=market_input, is_rising=1, top_n=5)

    html = render_to_string('dashboard/market_stocks.html', {
        'top_rising': top_rising,
        'top_falling': top_falling,
        'selected_market': market_input,
    })

    return JsonResponse({'html': html})
