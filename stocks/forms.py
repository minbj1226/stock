from django.db import models
from django.contrib.auth.models import User
from django import forms

class StockTransactionForm(forms.Form):
    stock_name = forms.CharField(required=False, label="종목명")
    quantity = forms.IntegerField(min_value=1, label="주문 수량")
    transaction_type = forms.ChoiceField(
        choices=[('buy', '매수'), ('sell', '매도')],
        widget=forms.RadioSelect,
        label="거래 유형"
    )