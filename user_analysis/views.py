from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import InvestmentProfile
from .forms import InvestmentTestForm
from django.core.exceptions import ObjectDoesNotExist

# 투자 성향 테스트 뷰 (CBV)
@method_decorator(login_required, name='dispatch')
class InvestmentTestView(View):
    def get(self, request):
        form = InvestmentTestForm()
        return render(request, "user_analysis/test.html", {"form": form})

    def post(self, request):
        form = InvestmentTestForm(request.POST)
        if form.is_valid():
            score = sum(int(value) for value in form.cleaned_data.values())

            # 점수에 따른 투자 성향 설정
            if score <= 10:
                risk_tolerance = "안정형"
            elif score <= 15:
                risk_tolerance = "안정추구형"
            elif score <= 20:
                risk_tolerance = "위험중립형"
            elif score <= 25:
                risk_tolerance = "적극투자형"
            else:
                risk_tolerance = "공격투자형"

            # 투자 성향 저장 (있으면 업데이트, 없으면 생성)
            investment_profile, created = InvestmentProfile.objects.get_or_create(user=request.user)
            investment_profile.risk_tolerance = risk_tolerance
            investment_profile.save()

            return redirect("user_analysis:result")  # 결과 페이지로 이동

        return render(request, "user_analysis/test.html", {"form": form})


# 투자 성향 결과 조회 뷰 (CBV)
@method_decorator(login_required, name='dispatch')
class InvestmentResultView(View):
    def get(self, request):
        try:
            investment_profile = InvestmentProfile.objects.get(user=request.user)
            risk_tolerance = investment_profile.risk_tolerance
        except ObjectDoesNotExist:
            return redirect("user_analysis:test")  # 프로필이 없으면 테스트 페이지로 이동

        return render(request, "user_analysis/result.html", {"risk_tolerance": risk_tolerance})
