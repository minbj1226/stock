import requests
from django.conf import settings

def get_stock_news(query="주식", display=4):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "date"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    return []


def get_market_indices():
    indices = {
        "0001": "코스피",
        "1001": "코스닥",
        "2001": "코스피200",
        "3001": "KRX150"
    }

    url = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {settings.ACCESS_TOKEN}",
        "appkey": settings.APP_KEY,
        "appsecret": settings.APP_SECRET,
        "tr_id": "FHKUP03500100"
    }

    market_data = []
    for iscd, name in indices.items():
        params = {
            "fid_cond_mrkt_div_code": "U",
            "fid_input_date_1": "20220411",
            "fid_input_date_2": "20220509",
            "fid_input_iscd": iscd,
            "fid_period_div_code": "D"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.json().get("rt_cd") == "0":
            output1 = response.json().get("output1", {})

            # 📌 데이터 변환
            current_price = float(output1.get("bstp_nmix_prpr", 0))  # 현재 지수
            price_change = float(output1.get("bstp_nmix_prdy_vrss", 0))  # 전일 대비 변화
            change_rate = float(output1.get("bstp_nmix_prdy_ctrt", 0))  # 전일 대비 변화율
            direction = "▲" if output1.get("prdy_vrss_sign") == "2" else "▼"  # 상승/하락 구분

            market_data.append({
                "name": name,
                "current_price": current_price,
                "price_change": f"{direction} {price_change}",
                "change_rate": f"{change_rate}%"
            })

    return market_data