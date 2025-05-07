from django.shortcuts import render
from recommend.services import recommend_stocks_by_profile
from accounts.models import InvestmentProfile
from .models import StockFundamental
from django.http import JsonResponse

def recommend_view(request):
    user = request.user
    try:
        profile_type = user.investment_profile.risk_tolerance
    except InvestmentProfile.DoesNotExist:
        profile_type = None

    if profile_type:
        stocks = recommend_stocks_by_profile(profile_type)
    else:
        stocks = []

    return render(request, 'recommend/recommend_list.html', {'stocks': stocks})