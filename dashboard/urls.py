from django.urls import path
from .views import index, ajax_market_stocks

app_name = 'dashboard'

urlpatterns = [
    path('', index, name="dashboard_index"),
    path('ajax/market/', ajax_market_stocks, name='ajax_market_stocks'),
]