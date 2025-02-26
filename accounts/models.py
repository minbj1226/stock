from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일을 고유 식별자로 사용

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# 투자 성향 프로필 (user_analysis 앱에서 관리)
class InvestmentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investment_profile')

    RISK_CHOICES = [
        ('안정형', '안정형'),
        ('안정추구형', '안정추구형'),
        ('위험중립형', '위험중립형'),
        ('적극투자형', '적극투자형'),
        ('공격투자형', '공격투자형'),
    ]
    risk_tolerance = models.CharField(max_length=20, choices=RISK_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.risk_tolerance}"