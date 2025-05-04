# recommend/management/commands/import_stock.py

from django.core.management.base import BaseCommand
import pandas as pd
from recommend.models import StockFundamental  # 모델 경로 확인 필수
import os

class Command(BaseCommand):
    help = 'CSV 파일을 읽어 StockFundamental 모델에 저장합니다.'

    def handle(self, *args, **kwargs):
        # BASE_DIR 기준 경로 (settings.py의 BASE_DIR 기준)
        csv_path = os.path.join("종목데이터.csv")  # 경로 필요 시 수정

        try:
            df = pd.read_csv(csv_path)

            objs = []
            for _, row in df.iterrows():
                if pd.isnull(row['ticker']) or pd.isnull(row['corp_name']) or pd.isnull(row['beta']) or pd.isnull(row['volatility']):
                    continue

                obj = StockFundamental(
                    ticker=row['ticker'],
                    corp_name=row['corp_name'],
                    market=row['market'],
                    stck_prpr=row['stck_prpr'],
                    per=row['per'],
                    pbr=row['pbr'],
                    eps=row['eps'],
                    bps=row['bps'],
                    volatility=row['volatility'],
                    beta=row['beta'],
                    market_cap=row['market_cap']
                )
                objs.append(obj)

            StockFundamental.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS("✅ DB 저장 완료"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 오류 발생: {e}"))