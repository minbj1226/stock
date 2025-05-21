from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from pykrx import stock
from datetime import datetime, timedelta
from .forms import StockTransactionForm
from pykis import PyKis
from .utils import get_stock_code_by_name
from .models import StockOrder

# TODO: 1. "pip install python-kis" 명령어 실행해주세요.
#          "pip install pykrx"
#          "python manage.py makemigrations stocks"
#          "python manage.py migrate"



# 자산 표시시
def get_balance_info():
    balance = kis.account().balance()

    purchase_amount = balance.purchase_amount or 0
    current_amount = balance.current_amount or 0
    profit = current_amount - purchase_amount
    profit_rate = (profit / purchase_amount) * 100 if purchase_amount else 0

    stock_details = [
        {
            "symbol": stock.symbol,
            "stock_name": stock.name,
            "qty": stock.qty,
            "purchase_price": stock.purchase_price,
            "current_price": stock.current_price,
            "profit": stock.profit,
            "profit_rate": stock.profit_rate,
        }
        for stock in balance.stocks
    ]

    return {
        "account_number": balance.account_number.number,
        "deposits": {
            "KRW": {"amount": balance.deposits["KRW"].amount}
        },
        "purchase_amount": purchase_amount,
        "current_amount": current_amount,
        "profit": profit,
        "profit_rate": profit_rate,
        "stocks": stock_details
    }


# 장 운영 시간
def is_market_open():
    trading_hours = kis.trading_hours("KR")
    now_kst = datetime.now().time()

    open_time = trading_hours.open_kst  # 이미 time 객체
    close_time = trading_hours.close_kst

    return open_time <= now_kst <= close_time


# TODO: 4. 로그인 기능을 사용하고 싶다면 아래 주석을 해제하세요.
@method_decorator(login_required, name='dispatch')
class StockTransactionView(View):
    def get(self, request):
        form = StockTransactionForm()
        balance_info = get_balance_info()
        orders = StockOrder.objects.filter().order_by('-created_at')

        return render(request, "mock_investment/transaction.html", {
            "form": form,
            "balance_info": balance_info,
            "orders": orders,
        })

    def post(self, request):
        form = StockTransactionForm(request.POST)
        balance_info = get_balance_info()

        if not is_market_open():
            messages.error(request, "❌ 현재는 장이 열려 있지 않습니다. 거래는 09:00~15:30에만 가능합니다.")
            orders = StockOrder.objects.filter(user=request.user).order_by('-created_at')
            return render(request, "mock_investment/transaction.html", {
                "form": form,
                "balance_info": balance_info,
                "orders": orders,
            })

        if form.is_valid():
            stock_name = form.cleaned_data['stock_name']
            quantity = form.cleaned_data['quantity']
            transaction_type = form.cleaned_data['transaction_type']

            stock_code = get_stock_code_by_name(stock_name)

            if not stock_code:
                messages.error(request, f"❌ 종목명을 찾을 수 없습니다: {stock_name}")
                return render(request, "mock_investment/transaction.html", {
                    "form": form,
                    "balance_info": balance_info,
                })

            try:
                stock = kis.stock(stock_code)
                if transaction_type == 'buy':
                    order = stock.buy(qty=quantity)
                    StockOrder.objects.create(
                        user=request.user,
                        stock_code=stock_code,
                        stock_name=stock_name,
                        quantity=quantity,
                        transaction_type='buy',
                        order_no=order.order_no
                    )
                    messages.success(request, f"✅ {stock_code} {quantity}주 매수 완료! (주문번호: {order.order_no})")
                else:
                    order = stock.sell(qty=quantity)
                    messages.success(request, f"✅ {stock_code} {quantity}주 매도 완료! (주문번호: {order.order_no})")
            except Exception as e:
                messages.error(request, f"❌ 주문 실패: {str(e)}")

            return redirect("mock_investment:transaction")

        orders = StockOrder.objects.all().order_by('-created_at')
        return render(request, "mock_investment/transaction.html", {
            "form": form,
            "balance_info": balance_info,
            "orders": orders,
        })


@require_POST
def cancel_order(request, order_id):
    try:
        order = StockOrder.objects.get(id=order_id)
        stock = kis.stock(order.stock_code)
        stock.cancel(order.order_no)

        order.delete()
        messages.success(request, f"❎ {order.stock_name} 주문이 취소되었습니다.")
    except Exception as e:
        messages.error(request, f"❌ 주문 취소 실패: {str(e)}")

    return redirect("mock_investment:transaction")


# 그래프 표시
def stock_chart_data(request):
    stock_name = request.GET.get("stock_name")
    if not stock_name:
        return JsonResponse({"error": "종목명이 필요합니다."}, status=400)

    try:
        stock_code = get_stock_code_by_name(stock_name)
        if not stock_code:
            return JsonResponse({"error": "해당 종목을 찾을 수 없습니다."}, status=404)

        end = datetime.today()
        start = end - timedelta(days=1080)
        df = stock.get_market_ohlcv_by_date(
            start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), stock_code
        )

        df.reset_index(inplace=True)
        df["date"] = df["날짜"].dt.strftime("%Y-%m-%d")

        close_prices = df["종가"].tolist()
        latest_close = close_prices[-1]
        previous_close = close_prices[-2] if len(close_prices) > 1 else latest_close

        price_change = latest_close - previous_close
        percent_change = (price_change / previous_close) * 100 if previous_close else 0

        chart_data = {
            "ticker": stock_code,
            "date": df["date"].tolist(),
            "open": df["시가"].tolist(),
            "high": df["고가"].tolist(),
            "low": df["저가"].tolist(),
            "close": close_prices,
            "volume": df["거래량"].tolist(),
            "latest_price": latest_close,
            "price_change": price_change,
            "percent_change": percent_change,
        }
        return JsonResponse(chart_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)