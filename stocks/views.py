from django.shortcuts import render, get_object_or_404
from recommend.models import StockFundamental
from django.http import JsonResponse
from datetime import datetime, timedelta
from pykrx import stock
import requests
from django.conf import settings

def stock_chart_api(request, ticker):
    today = datetime.today().strftime('%Y%m%d')
    three_years_ago = (datetime.today() - timedelta(days=1080)).strftime('%Y%m%d')

    try:
        df = stock.get_market_ohlcv_by_date(three_years_ago, today, ticker)
        df = df.reset_index()
        df = df.rename(columns={
            '날짜': 'date',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '종가': 'close',
            '거래량': 'volume'
        })
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

        data = {
            'date': df['date'].tolist(),
            'open': df['open'].tolist(),
            'high': df['high'].tolist(),
            'low': df['low'].tolist(),
            'close': df['close'].tolist(),
            'volume': df['volume'].tolist(),
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def stock_search(request):
    query = request.GET.get('query', '')
    if query:
        stocks = StockFundamental.objects.filter(corp_name__icontains=query).values('corp_name', 'ticker')
    else:
        stocks = []

    return JsonResponse(list(stocks), safe=False)

def stock_detail(request, ticker):
    stock = get_object_or_404(StockFundamental, ticker=ticker)
    news = get_stock_news(stock.corp_name)
    return render(request, 'stocks/stock_detail.html', {
        'stock': stock,
        'news': news
    })

def get_stock_news(query="주식", display=10):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
    }
    params = {
        "query": query + " 주식",  # ex: "삼성전자 주식"
        "display": display,
        "sort": "date"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    return []