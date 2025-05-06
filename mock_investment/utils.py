import numpy as np
from pykrx import stock
from datetime import datetime

def get_stock_code_by_name(stock_name: str) -> str:
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        print(f"오늘 날짜: {today}")
        print(f"종목명: {stock_name}")

        tickers = stock.get_market_ticker_list(date=today, market="ALL")
        name_to_code = {stock.get_market_ticker_name(ticker): ticker for ticker in tickers}
        code = name_to_code.get(stock_name)

        print(f"{stock_name}의 종목코드는: {code}")
        return code
    except:
        print(f"종목코드({stock_name})를 찾을 수 없습니다.")
        return None
