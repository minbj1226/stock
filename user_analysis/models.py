from django.db import models
from accounts.models import User

class Question(models.Model):
    number = models.PositiveIntegerField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Q{self.number}: {self.text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    value = models.IntegerField()  # 점수

    def __str__(self):
        return f"{self.text} ({self.value})"

class InvestmentAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']
