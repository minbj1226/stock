import requests
from django.conf import settings
from dashboard.utils.token_manager import ACCESS_TOKEN, ACCESS_LIVE_TOKEN

def get_stock_news(query="주식", display=8):
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
        "2001": "코스피200"
    }

    url = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {ACCESS_TOKEN.get_token()}",
        "appkey": settings.APP_KEY,
        "appsecret": settings.APP_SECRET,
        "tr_id": "FHKUP03500100"
    }

    market_data = []
    for iscd, name in indices.items():
        params = {
            "fid_cond_mrkt_div_code": "U",
            "fid_input_date_1": "20250310",
            "fid_input_date_2": "20250624",
            "fid_input_iscd": iscd,
            "fid_period_div_code": "D"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.json().get("rt_cd") == "0":
            output2 = response.json().get("output2", [])

            # 📈 미니 차트용 시계열 데이터 구성
            chart_data = [float(item["bstp_nmix_prpr"]) for item in output2 if item.get("bstp_nmix_prpr")][::-1]

            output1 = response.json().get("output1", {})
            current_price = float(output1.get("bstp_nmix_prpr", 0))
            price_change = float(output1.get("bstp_nmix_prdy_vrss", 0))
            change_rate = float(output1.get("bstp_nmix_prdy_ctrt", 0))
            direction = "▲" if output1.get("prdy_vrss_sign") == "2" else "▼"

            market_data.append({
                "name": name,
                "current_price": current_price,
                "price_change": f"{direction} {price_change}",
                "change_rate": f"{change_rate}%",
                "chart_data": chart_data
            })

    return market_data

def get_top_movers(market="", is_rising=0, top_n=5):
    API_URL = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/ranking/fluctuation"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {ACCESS_LIVE_TOKEN.get_token()}",
        "appkey": settings.APP_LIVE_KEY,
        "appsecret": settings.APP_LIVE_SECRET,
        "tr_id": "FHPST01700000"
    }

    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_cond_scr_div_code": "20170",
        "fid_input_iscd": market,
        "fid_rank_sort_cls_code": is_rising,  # 상승 = "0", 하락 = "1"
        "fid_input_cnt_1": str(top_n),
        "fid_prc_cls_code": "0",
        "fid_input_price_1": "",
        "fid_input_price_2": "",
        "fid_vol_cnt": "",
        "fid_trgt_cls_code": "0",
        "fid_trgt_exls_cls_code": "0",
        "fid_div_cls_code": "0",
        "fid_rsfl_rate1": "",
        "fid_rsfl_rate2": ""
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if "rt_cd" in data and data["rt_cd"] == "0":
            items = data.get("output", [])

            reverse_order = is_rising == 0

            sorted_items = sorted(items, key=lambda x: float(x['prdy_ctrt']), reverse=reverse_order)

            result = []
            for idx, item in enumerate(sorted_items[:top_n], start=1):
                result.append({
                    "순위": idx,
                    "종목명": item["hts_kor_isnm"],  # 종목명
                    "현재가": int(item["stck_prpr"]),  # 현재가
                    "등락": f"{int(item['prdy_vrss'])} ({item['prdy_ctrt']}%)"  # 등락률
                })
            return result
        else:
            print(f"API 오류: {data}")
            return []
    else:
        print(f"HTTP 오류: {response.status_code}, 응답: {response.text}")
        return []