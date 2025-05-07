# stocks/urls.py
from django.urls import path
from . import views

app_name='stocks'

urlpatterns = [
    path('stock_search/', views.stock_search, name='stock_search'),  # 주식 검색
    path('<str:ticker>/', views.stock_detail, name='stock_detail'),  # 주식 상세 페이지
]