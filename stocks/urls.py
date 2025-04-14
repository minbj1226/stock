from django.urls import path
from .views import StockTransactionView

app_name ='stocks'

urlpatterns = [
    path('transaction/', StockTransactionView.as_view(), name='transaction'),
]