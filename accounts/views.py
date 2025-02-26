from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm

# 회원가입 뷰
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect("user_analysis:test")  # 회원가입 후 설문 페이지로 이동
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})

# 로그인 뷰 (Django 기본 LoginView 사용)
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

# 로그아웃 뷰 (Django 기본 LogoutView 사용)
class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"
