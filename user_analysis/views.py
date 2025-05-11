from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import InvestmentProfile
from .models import Question, Choice, InvestmentAnswer
from django.utils import timezone

def get_risk_tolerance(score):
    if score <= 20:
        return "안정형"
    elif score <= 40:
        return "안정추구형"
    elif score <= 60:
        return "위험중립형"
    elif score <= 80:
        return "적극투자형"
    else:
        return "공격투자형"

class IntroView(TemplateView):
    template_name = "user_analysis/intro.html"

@method_decorator(login_required, name='dispatch')
class InvestmentTestView(View):
    def get(self, request, step):
        question = get_object_or_404(Question, number=step)
        total = Question.objects.count()
        progress = int((step/total)* 100)
        remain = total - step
        return render(request, "user_analysis/step.html", {
            "question": question,
            "step": int(step),
            "total": total,
            "progress": progress,
            'remain': remain
        })

    def post(self, request, step):
        question = get_object_or_404(Question, number=step)
        selected_choice = get_object_or_404(Choice, id=request.POST.get("choice"), question=question)

        # 중복 응답 존재 여부 확인 및 저장/수정
        answer, created = InvestmentAnswer.objects.get_or_create(
            user=request.user,
            question=question,
            defaults={'selected_choice': selected_choice}
        )
        if not created:
            # 이미 응답이 존재하면 선택지만 업데이트
            answer.selected_choice = selected_choice
            answer.submitted_at = timezone.now()
            answer.save()

        # 다음 질문 또는 결과 페이지로 이동
        next_step = step + 1
        if next_step <= Question.objects.count():
            return redirect("user_analysis:question_step", step=next_step)
        return redirect("user_analysis:result")

@method_decorator(login_required, name='dispatch')
class InvestmentResultView(View):
    def get(self, request):
        # 전체 응답 불러오기 및 점수 계산
        answers = InvestmentAnswer.objects.filter(user=request.user).select_related("selected_choice")
        total_score = sum(ans.selected_choice.value for ans in answers)
        risk_tolerance = get_risk_tolerance(total_score)

        # InvestmentProfile에 저장 (없으면 생성)
        profile, _ = InvestmentProfile.objects.get_or_create(user=request.user)
        profile.risk_tolerance = risk_tolerance
        profile.save()

        return render(request, "user_analysis/result.html", {
            "risk_tolerance": risk_tolerance,
            "total_score": total_score
        })

