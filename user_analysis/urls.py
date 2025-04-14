from django.urls import path
from .views import InvestmentTestView, InvestmentResultView, IntroView

app_name ='user_analysis'

urlpatterns = [
    path('intro/', IntroView.as_view(), name='intro'),
    path('test/<int:step>/', InvestmentTestView.as_view(), name='question_step'),
    path('result/', InvestmentResultView.as_view(), name='result')
]