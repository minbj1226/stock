from django.shortcuts import render
from recommend.services import recommend_stocks_by_profile
from accounts.models import InvestmentProfile

# 시가총액 단위 변환 함수
def format_market_cap(value):
    try:
        value = int(str(value).replace(",", ""))
    except (ValueError, TypeError):
        return "N/A"

    if value >= 10_000:  # 1조 이상 (1만 억 이상)
        return f"{value / 10_000:.1f}조원"
    else:
        return f"{value:,}억원"

PROFILE_TYPE_DESCRIPTION = {
    "공격투자형": """• 1년 변동성 > 30% 또는 β > 1.5
• 시가총액 하위 50% (스몰캡)
• 적자·고성장 섹터 (바이오, AI 등)""",
    "적극투자형": """• 변동성 20~30%, β 1.2~1.5
• 중소형주 (KOSDAQ 중심)
• 최근 3년 매출·EPS 성장률 > 15%""",
    "위험중립형": """• 변동성 10~20%, β 1.0~1.2
• KOSPI 200 & KOSDAQ150 중심
• 성장 + 배당 혼합 (배당수익률 ≥ 1%)""",
    "안정추구형": """• 변동성 10~18%, β ≤ 1.0
• 대형주 (코스피100) 우량 중심
• 배당수익률 ≥ 2%, 부채비율 ≤ 100%""",
    "안정형": """• 변동성 ≤ 12%, β ≤ 0.8
• 코스피50 블루칩 (은행·통신·유틸)
• 배당수익률 ≥ 3%, 최근 5년 연속 흑자"""
}

def recommend_view(request):
    user = request.user
    try:
        profile_type = user.investment_profile.risk_tolerance
    except InvestmentProfile.DoesNotExist:
        profile_type = None

    profile_description = PROFILE_TYPE_DESCRIPTION.get(profile_type, "")

    stocks = []
    if profile_type:
        all_stocks = recommend_stocks_by_profile(profile_type)

        # per, pbr 값이 None 또는 0이 아닌 것만 필터링
        stocks = [
            stock for stock in all_stocks
            if stock.per not in [None, 0, 0.0] and stock.pbr not in [None, 0, 0.0]
        ]

        # 시가총액 단위 포맷 적용
        for stock in stocks:
            stock.market_cap = int(stock.market_cap)
            stock.formatted_market_cap = format_market_cap(stock.market_cap)

    return render(request, 'recommend/recommend_list.html', {
        'stocks': stocks,
        'profile_type': profile_type,
        'profile_description': profile_description,
    })
