from django.shortcuts import render, get_object_or_404
from recommend.models import StockFundamental
from django.http import JsonResponse

def stock_search(request):
    query = request.GET.get('query', '')
    if query:
        stocks = StockFundamental.objects.filter(corp_name__icontains=query).values('corp_name', 'ticker')
    else:
        stocks = []

    return JsonResponse(list(stocks), safe=False)

def stock_detail(request, ticker):
    stock = get_object_or_404(StockFundamental, ticker=ticker)
    return render(request, 'stocks/stock_detail.html', {'stock': stock})