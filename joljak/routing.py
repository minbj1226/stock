from django.urls import re_path
from dashboard.consumers import StockIndexConsumer

websocket_urlpatterns = [
    re_path(r"ws/stock_index/$", StockIndexConsumer.as_asgi()),
]
