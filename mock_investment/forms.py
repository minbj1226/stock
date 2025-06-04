from django import forms

class StockTransactionForm(forms.Form):
    stock_name = forms.CharField(widget=forms.HiddenInput())  # 종목명은 고정값으로 받는 경우
    transaction_type = forms.CharField(widget=forms.HiddenInput())  # 매수/매도
    price_type = forms.ChoiceField(
        choices=[('limit', '지정가'), ('market', '시장가')],
        widget=forms.HiddenInput()
    )
    price = forms.IntegerField(required=False)  # 지정가만 필요
    quantity = forms.IntegerField(min_value=1, initial=1)