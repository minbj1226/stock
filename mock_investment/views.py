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

# TODO: 2. 실전 투자는 모의 투자를 주석처리하고 실전 투자 코드를 사용하세요.
# 한국투자증권 API 인증 객체 로드 (실전 투자)
kis = PyKis(

)

# TODO: 3. 모의 투자는 실전 투자를 주석처리하고 모의 투자 코드를 사용하세요.
# 한국투자증권 API 인증 객체 로드 (모의 투자)
#kis = PyKis(
#   id="@2148424",
#    account="50131449-01",
#    appkey="PS8Mg5C875dma63mmwCd4tIiSMakLCxJB1FC",
#    secretkey="2LUx2qzS8PJUMP8j+d/OSlcHL5H92L3THIBZygs0IYtk+SgDoEb8CO/3eGJSoOcVdmgaP3JnWFcbP49zPOaEffQS8LoQ8rSasYndNBB5l4bGzj7oeDft0M1seUnvOgU3pV8qFEaK9qRHyjd5zOnkB0RGUqVAbIKjebDIzM5iG1HELGfenAw=",  # 실전투자 SecretKey 180자리
#    virtual_id="@2148424",
#    virtual_appkey="PSYgddKm8LTX0L9wjSKxwrzXAWAaIdOLV87G",
#    virtual_secretkey="2Dgjsn5O9Bqeb17g4+w14D3sr3//KWLM/mlClFC/Ol3Vn4S4C4pchM1pJAbRmxZCH3j/tlgwZio+jsZI4s/fCIDSFVtbdQG3lPO7LRGu5y6JY3UK/7yjvGdpSPHqblrmp/j8LsKBVUhvLKA+Dqf7QGRFs6mcdnrUAzHF/+pKIunhL33KIlg=",  # 모의투자 SecretKey 180자리
#    keep_token=True,
#)

# TODO: 4. 로그인 기능을 사용하고 싶다면 아래 주석을 해제하세요.
# @method_decorator(login_required, name='dispatch')
class StockTransactionView(View):
    def get(self, request):
        form = StockTransactionForm()
        balance = kis.account().balance()

        balance_info = {
            "account_number": balance.account_number.number,
            "deposits": {
                "KRW": {"amount": balance.deposits["KRW"].amount}
            },
            "purchase_amount": balance.purchase_amount,
            "current_amount": balance.current_amount,
            "profit": balance.profit,
            "profit_rate": balance.profit_rate * 100
        }

        orders = StockOrder.objects.all().order_by('-created_at')
        return render(request, "mock_investment/transaction.html", {
            "form": form,
            "balance_info": balance_info,
            "orders": orders,
        })

    def post(self, request):
        form = StockTransactionForm(request.POST)
        balance = kis.account().balance()

        balance_info = {
            "account_number": balance.account_number.number,
            "deposits": {
                "KRW": {"amount": balance.deposits["KRW"].amount}
            },
            "purchase_amount": balance.purchase_amount,
            "current_amount": balance.current_amount,
            "profit": balance.profit,
            "profit_rate": balance.profit_rate * 100
        }

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

def stock_chart_data(request):
    stock_name = request.GET.get("stock_name")
    if not stock_name:
        return JsonResponse({"error": "종목명이 필요합니다."}, status=400)

    try:
        stock_code = get_stock_code_by_name(stock_name)
        if not stock_code:
            return JsonResponse({"error": "해당 종목을 찾을 수 없습니다."}, status=404)

        end = datetime.today()
        start = end - timedelta(days=30)
        df = stock.get_market_ohlcv_by_date(
            start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), stock_code
        )

        df.reset_index(inplace=True)
        df["date"] = df["날짜"].dt.strftime("%Y-%m-%d")

        chart_data = {
            "date": df["date"].tolist(),
            "open": df["시가"].tolist(),
            "high": df["고가"].tolist(),
            "low": df["저가"].tolist(),
            "close": df["종가"].tolist(),
        }

        return JsonResponse(chart_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
