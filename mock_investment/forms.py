from django.db import models
from django.contrib.auth.models import User
from django import forms

class StockTransactionForm(forms.Form):
    stock_name = forms.CharField(required=False, label="종목명")
    quantity = forms.IntegerField(min_value=1, label="주문 수량")
    transaction_type = forms.CharField(widget=forms.HiddenInput())