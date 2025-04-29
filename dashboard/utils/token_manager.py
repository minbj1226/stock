import requests
import json
from django.conf import settings
from django.core.cache import cache

class TokenManager:
    def __init__(self, app_key, app_secret, is_live=False):
        self.is_live = is_live
        self.app_key = app_key
        self.app_secret = app_secret
        self.token_url = (
            "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
            if is_live else
            "https://openapivts.koreainvestment.com:29443/oauth2/tokenP"
        )

    def get_token(self):
        cache_key = "kis_access_token_live" if self.is_live else "kis_access_token_virtual"
        token = cache.get(cache_key)

        if token is None:
            token = self.refresh_token()

        return token

    def refresh_token(self):
        headers = {
            "content-type": "application/json"
        }
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        # ✅ body를 json.dumps()로 보내야 해
        response = requests.post(self.token_url, headers=headers, data=json.dumps(body))

        if response.status_code != 200:
            raise Exception(f"HTTP 요청 실패: {response.status_code} {response.text}")

        data = response.json()

        if "access_token" in data:
            token = data["access_token"]
            expires_in = int(data.get("expires_in", 3600))  # 기본 1시간
            cache_key = "kis_access_token_live" if self.is_live else "kis_access_token_virtual"
            cache.set(cache_key, token, timeout=expires_in - 60)  # 60초 여유
            print(f"✅ [{cache_key}] 토큰 발급 완료")
            return token
        else:
            error_message = data.get('msg1', 'Unknown error')
            raise Exception(f"토큰 발급 실패: {error_message}")

# 전역으로 준비 (토큰 자체가 아니라 매니저)
ACCESS_TOKEN = TokenManager(settings.APP_KEY, settings.APP_SECRET, is_live=False)
ACCESS_LIVE_TOKEN = TokenManager(settings.APP_LIVE_KEY, settings.APP_LIVE_SECRET, is_live=True)
