from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import StockTransactionForm
from pykis import PyKis

# TODO: 1. "pip install python-kis" 명령어 실행해주세요.

# TODO: 2. 실전 투자는 모의 투자를 주석처리하고 실전 투자 코드를 사용하세요.
# 한국투자증권 API 인증 객체 로드 (실전 투자)
kis = PyKis(
    id="minbj26",  # HTS 로그인 ID
    account="73071159-01",  # 계좌번호
    appkey="PSaxZrRqDLyginQGGy8DZRqU5xKUmwiyU4iF",  # AppKey 36자리
    secretkey="9j+4SU9zHYL0BdTpLXmCKC8pb6Kq8ErLqltEUqelbexdnZDm1LWUqiNGHA0zH84MuCBSO6xlUzYmSh1zAlFyx6P3U0ZdDPAMoKh4Exx4wFMRY2ligzFdyWMjvDcdw95pAonXeaIAvsLyV7cbbiYb/r6yshv7kgnBYl+nHL8QYXKkdMcvdCw=",  # SecretKey 180자리
    keep_token=True,  # API 접속 토큰 자동 저장
)

# TODO: 3. 모의 투자는 실전 투자를 주석처리하고 모의 투자 코드를 사용하세요.
# 한국투자증권 API 인증 객체 로드 (모의 투자)
#kis = PyKis(
#    id="minbj26",
#    account="50124825-01",
#    appkey="PSp7psitoiWzFj6LURnXcAOFm3mqTR0wYdvg",
#    secretkey="2LUx2qzS8PJUMP8j+d/OSlcHL5H92L3THIBZygs0IYtk+SgDoEb8CO/3eGJSoOcVdmgaP3JnWFcbP49zPOaEffQS8LoQ8rSasYndNBB5l4bGzj7oeDft0M1seUnvOgU3pV8qFEaK9qRHyjd5zOnkB0RGUqVAbIKjebDIzM5iG1HELGfenAw=",  # 실전투자 SecretKey 180자리
#    virtual_id="minbj26",
#    virtual_appkey="PSp7psitoiWzFj6LURnXcAOFm3mqTR0wYdvg",
#    virtual_secretkey="CxpywGdg9FE1wYrglWRW42wLL2Rfyjap6pLJSnqVIrWhPlWBzIKE1hpNEFVOIAzWYvRzLR+QIUXTZlG5zdgYD+yvUijEL7qu1Niqqf+3yEoFm8IBPdwTxSg5aXeifH0r+I2gnn/tU0CddVx9cX16uImgETTxtkVdUzg/V54O0GlSVZPW4OM=",  # 모의투자 SecretKey 180자리
#    keep_token=True,
#)

@method_decorator(login_required, name='dispatch')
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

        return render(request, "stocks/transaction.html", {
            "form": form,
            "balance_info": balance_info,
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
            stock_code = form.cleaned_data['stock_code']
            quantity = form.cleaned_data['quantity']
            transaction_type = form.cleaned_data['transaction_type']

            try:
                stock = kis.stock(stock_code)
                if transaction_type == 'buy':
                    order = stock.buy(qty=quantity)
                    messages.success(request, f"✅ {stock_code} {quantity}주 매수 완료! (주문번호: {order.order_no})")
                else:
                    order = stock.sell(qty=quantity)
                    messages.success(request, f"✅ {stock_code} {quantity}주 매도 완료! (주문번호: {order.order_no})")
            except Exception as e:
                messages.error(request, f"❌ 주문 실패: {str(e)}")
            
            return redirect("stocks:transaction")

        return render(request, "stocks/transaction.html", {
            "form": form,
            "balance_info": balance_info,
        })