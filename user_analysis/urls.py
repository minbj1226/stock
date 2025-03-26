from django.urls import path
from .views import InvestmentTestView, InvestmentResultView

app_name ='user_analysis'

urlpatterns = [
    path('test/', InvestmentTestView.as_view(), name='test'),
    path('result/', InvestmentResultView.as_view(), name='result')
]