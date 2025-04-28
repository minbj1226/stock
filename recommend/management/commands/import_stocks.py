# recommend/management/commands/import_stocks.py

from django.core.management.base import BaseCommand
import pandas as pd
from recommend.models import StockFundamental

class Command(BaseCommand):
    help = '종목코드1.csv와 종목펀더멘탈.csv를 합쳐서 StockFundamental 모델에 저장'

    def handle(self, *args, **options):
        # 1. CSV 불러오기
        basic_df = pd.read_csv('종목코드1.csv')  # ticker, corp_name, market
        fundamental_df = pd.read_csv('종목펀더멘탈.csv')  # ticker, per, pbr, eps, bps, stck_prpr

        # 2. 필요한 컬럼만 남기고 NaN 데이터는 제외
        fundamental_df = fundamental_df[['ticker', 'per', 'pbr', 'eps', 'bps', 'stck_prpr']]  # roe, dps, dividend_yield 빼버림

        # 3. ticker 기준으로 merge
        merged_df = pd.merge(basic_df, fundamental_df, on='ticker', how='inner')

        # 4. DB에 저장
        save_count = 0
        for _, row in merged_df.iterrows():
            StockFundamental.objects.update_or_create(
                ticker=row['ticker'],
                defaults={
                    'corp_name': row['corp_name'],
                    'market': row['market'],
                    'stck_prpr': row.get('stck_prpr'),
                    'per': row.get('per'),
                    'pbr': row.get('pbr'),
                    'eps': row.get('eps'),
                    'bps': row.get('bps'),
                }
            )
            save_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ {save_count}개 종목 저장 완료!'))
