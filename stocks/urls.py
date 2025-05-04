from django.urls import path
from .views import StockTransactionView, cancel_order, stock_chart_data

app_name = 'stocks'

urlpatterns = [
    path('transaction/', StockTransactionView.as_view(), name='transaction'),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('stock_chart_data/', stock_chart_data, name='stock_chart_data'),
]
