from django import forms

class InvestmentTestForm(forms.Form):
    q1 = forms.ChoiceField(
        label="1. 당신의 연령대는 어떻게 되나요?",
        choices=[
            (1, "19세 이하"),
            (2, "20세~40세"),
            (3, "41세~50세"),
            (4, "51세~60세"),
            (5, "61세 이상"),
        ],
        widget=forms.RadioSelect
    )

    q2 = forms.ChoiceField(
        label="2. 투자하고자 하는 돈을 얼마나 오래 투자할 계획인가요?",
        choices=[
            (1, "6개월 이하"),
            (2, "6개월~1년 이하"),
            (3, "1년~2년 이하"),
            (4, "2년~3년 이하"),
            (5, "3년 이상"),
        ],
        widget=forms.RadioSelect
    )

    q3 = forms.MultipleChoiceField(
        label="3. 당신이 해본 투자 경험 중 가장 가까운 것은 무엇인가요? (중복 선택 가능)",
        choices=[
            (1, "예금, 적금, 국채, 지방채 등"),
            (2, "회사채, 채권형 펀드, 원금보장형 ELS 등"),
            (3, "원금 일부 보장형 ELS, 혼합형 펀드 등"),
            (4, "주식, 원금 비보장형 ELS, 시장 수익률 펀드 등"),
            (5, "선물옵션, 파생상품, 주식 신용거래 등"),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    q4 = forms.ChoiceField(
        label="4. 금융 및 투자에 대한 본인의 지식수준은 어느 정도라고 생각하나요?",
        choices=[
            (1, "전혀 몰라요! 금융상품도 잘 몰라요."),
            (2, "기본적인 예금과 적금 정도는 알아요."),
            (3, "주식과 펀드 차이를 알고, 어느 정도 투자 경험이 있어요."),
            (4, "경제 뉴스나 기업 분석을 보고 투자할 수 있어요."),
            (5, "전문 투자자 수준! 직접 주식과 자산을 분석해요."),
        ],
        widget=forms.RadioSelect
    )

    q5 = forms.ChoiceField(
        label="5. 현재 투자하고자 하는 자금은 전체 자산에서 어느 정도의 비율을 차지하나요?",
        choices=[
            (1, "10% 이하"),
            (2, "10%~20% 이하"),
            (3, "20%~30% 이하"),
            (4, "30%~40% 이하"),
            (5, "40% 이상"),
        ],
        widget=forms.RadioSelect
    )

    q6 = forms.ChoiceField(
        label="6. 다음 중 당신의 수입원을 가장 잘 나타내고 있는 것은 어느 것 인가요?",
        choices=[
            (1, "현재 일정한 수입이 발생, 향후 현재 수준을 유지하거나 증가해요."),
            (2, "현재 일정한 수입이 발생, 향후 감소하거나 불안정해요."),
            (3, "현재 일정한 수입이 없어요.")
        ],
        widget=forms.RadioSelect
    )

    q7 = forms.ChoiceField(
        label ="7. 만약 투자원금에 손실이 발생할 경우 다음 중 감수할 수 있는 손실 수준은 어느 것 인가요?",
        choices=[
            (1, "무슨 일이 있어도 투자원금은 보전되어야 해요."),
            (2, "10% 미만까지는 손실을 감수할 수 있어요"),
            (3, "20% 미만까지는 손실을 감수할 수 있어요"),
            (4, "기대수익이 높다면 위험이 높아도 괜찮아요")
        ],
        widget=forms.RadioSelect
    )