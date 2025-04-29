from .utils import recommend_stocks_by_profile
from django.shortcuts import render, get_object_or_404
from accounts.models import InvestmentProfile

def recommend_view(request):
    user = request.user

    # 1. 로그인한 사용자의 투자성향 찾기
    investment_profile = get_object_or_404(InvestmentProfile, user=user)
    profile_type = investment_profile.risk_tolerance

    # 2. 추천 종목 가져오기
    recommended_stocks = recommend_stocks_by_profile(profile_type, count=5)

    return render(request, 'recommend/recommend_list.html', {
        'stocks': recommended_stocks,
        'profile_type': profile_type,
    })
