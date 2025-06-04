from django.core.management.base import BaseCommand
import pandas as pd
from recommend.models import StockFundamental  # 모델 경로 확인 필수
import os

class Command(BaseCommand):
    help = 'CSV 파일을 읽어 StockFundamental 모델에 update_or_create로 저장합니다.'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join("종목데이터.csv")

        try:
            df = pd.read_csv(csv_path)

            for _, row in df.iterrows():
                if pd.isnull(row['ticker']) or pd.isnull(row['corp_name']) or pd.isnull(row['beta']) or pd.isnull(row['volatility']):
                    continue

                StockFundamental.objects.update_or_create(
                    ticker=row['ticker'],
                    defaults={
                        'corp_name': row['corp_name'],
                        'market': row['market'],
                        'stck_prpr': row['stck_prpr'],
                        'per': row['per'],
                        'pbr': row['pbr'],
                        'eps': row['eps'],
                        'bps': row['bps'],
                        'volatility': row['volatility'],
                        'beta': row['beta'],
                        'market_cap': row['market_cap'],
                        'sector': row['sector'],
                    }
                )

            self.stdout.write(self.style.SUCCESS("✅ DB update_or_create 완료"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 오류 발생: {e}"))
