from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import InvestmentProfile
from .forms import InvestmentTestForm
from django.core.exceptions import ObjectDoesNotExist

# 점수 매핑
SCORE_MAPPING = {
    "q1": {1: 12.5, 2: 12.5, 3: 9.3, 4: 6.2, 5: 3.1},
    "q2": {1: 3.1, 2: 6.2, 3: 9.3, 4: 12.5, 5: 15.6},
    "q3": {1: 3.1, 2: 6.2, 3: 9.3, 4: 12.5, 5: 15.6},
    "q4": {1: 3.1, 2: 6.2, 3: 9.3, 4: 12.5, 5: 18.7},
    "q5": {1: 15.6, 2: 12.5, 3: 9.3, 4: 6.2, 5: 3.1},
    "q6": {1: 9.3, 2: 6.2, 3: 3.1},
    "q7": {1: -6.2, 2: 6.2, 3: 12.5, 4: 18.7},
}

def calculate_score(form_data):
    total_score = 0
    for key, value in form_data.items():
        if key == "q3":  # 다중 선택 처리
            total_score += sum(SCORE_MAPPING[key].get(int(v), 0) for v in value)
        else:
            total_score += SCORE_MAPPING[key].get(int(value), 0)
    return total_score

# 투자 성향 테스트 뷰 (CBV)
@method_decorator(login_required, name='dispatch')
class InvestmentTestView(View):
    def get(self, request):
        form = InvestmentTestForm()
        return render(request, "user_analysis/test.html", {"form": form})

    def post(self, request):
        form = InvestmentTestForm(request.POST)
        if form.is_valid():
            score = calculate_score(form.cleaned_data)  # 수정된 점수 계산 함수 적용

            # 점수에 따른 투자 성향 설정
            if score <= 20:
                risk_tolerance = "안정형"
            elif score <= 40:
                risk_tolerance = "안정추구형"
            elif score <= 60:
                risk_tolerance = "위험중립형"
            elif score <= 80:
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


