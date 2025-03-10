import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer

class StockIndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """웹소켓 연결 시 실행"""
        await self.accept()
        self.send_task = asyncio.create_task(self.send_stock_data())

    async def disconnect(self, close_code):
        """웹소켓 연결 종료 시 실행"""
        if self.send_task:
            self.send_task.cancel()

    async def send_stock_data(self):
        """한국투자증권 API에서 데이터를 가져와 클라이언트에 전송"""
        while True:
            stock_data = await self.fetch_stock_data()
            await self.send(json.dumps(stock_data))
            await asyncio.sleep(5)  # 5초마다 데이터 전송

    async def fetch_stock_data(self):
        """API 호출을 통해 실시간 주가지수 데이터 가져오기"""
        url = "https://api.koreainvestment.com/uapi/domestic-stock/v1/quotations/index"
        headers = {
            "authorization": "Bearer YOUR_ACCESS_TOKEN",
            "appkey": "YOUR_APP_KEY",
            "appsecret": "YOUR_APP_SECRET",
            "tr_id": "FHKST01010100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 국내 주식시장 (코스피, 코스닥 등)
            "FID_INPUT_ISCD": "0001",  # 코스피 (0001), 코스닥 (1001)
        }

        async with asyncio.get_event_loop().run_in_executor(None, requests.get, url, headers, params) as response:
            data = response.json()
            return {
                "kospi": data["output"]["stck_prpr"],  # 현재 지수
                "kosdaq": data["output"]["prdy_vrss"],  # 변동 폭
            }
