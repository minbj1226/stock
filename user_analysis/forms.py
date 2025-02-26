from django import forms

RISK_CHOICES = [
    (1, "A. 안전한 선택! 무조건 손실이 없는 길을 택한다."),
    (2, "B. 적당한 모험! 리스크가 있지만 수익도 노려본다."),
    (3, "C. 고위험 고수익! 잃어도 괜찮아, 크게 벌어보자!"),
]

class InvestmentTestForm(forms.Form):
    question1 = forms.ChoiceField(
        label="1. 길 가다가 복권을 발견했다! 당신의 선택은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question2 = forms.ChoiceField(
        label="2. 친구가 '이 주식 꼭 오른다!'라고 추천했다. 당신의 반응은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question3 = forms.ChoiceField(
        label="3. 1억이 생긴다면 가장 먼저 할 행동은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question4 = forms.ChoiceField(
        label="4. 놀이공원에서 가장 먼저 타고 싶은 놀이기구는?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question5 = forms.ChoiceField(
        label="5. 5년 동안 돈을 모아야 한다면?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question6 = forms.ChoiceField(
        label="6. 주식 시장이 급락했다! 당신의 대응은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question7 = forms.ChoiceField(
        label="7. 친구들과 카드 게임을 한다면 어떤 전략을 택할까?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question8 = forms.ChoiceField(
        label="8. 해외여행을 갈 때 당신의 스타일은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question9 = forms.ChoiceField(
        label="9. 식당에서 메뉴를 고를 때 당신의 기준은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
    question10 = forms.ChoiceField(
        label="10. 돈을 빌려준 친구가 아직도 돈을 안 갚고 있다! 당신의 반응은?",
        choices=RISK_CHOICES,
        widget=forms.RadioSelect
    )
