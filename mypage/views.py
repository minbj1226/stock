from django.shortcuts import render
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from accounts.models import InvestmentProfile
from user_analysis.models import InvestmentAnswer
from mock_investment.views import get_balance_info

@login_required
def mypage(request):
    profile = InvestmentProfile.objects.get(user=request.user)
    last_answer = InvestmentAnswer.objects.filter(user=request.user).order_by('-submitted_at').first()

    try:
        balance_info = get_balance_info()
    except Exception:
        balance_info = None

    return render(request, 'mypage/mypage.html', {
        'investment_type': profile.risk_tolerance,
        'last_test_date': localtime(last_answer.submitted_at) if last_answer else None,
        'balance_info': balance_info,
        "mock_results": balance_info["stocks"]
    })