from django.shortcuts import render
from recommend.services import recommend_stocks_by_profile
from accounts.models import InvestmentProfile

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

    top5 = stocks[:5]
    others = stocks[5:]

    return render(request, 'recommend/recommend_list.html', {'top5': top5, 'others': others})