from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # 커스텀 User 모델 사용

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
