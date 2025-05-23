# Generated by Django 5.1.6 on 2025-04-30 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockFundamental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('corp_name', models.CharField(max_length=100)),
                ('market', models.CharField(max_length=10)),
                ('stck_prpr', models.IntegerField(blank=True, null=True)),
                ('per', models.FloatField(blank=True, null=True)),
                ('pbr', models.FloatField(blank=True, null=True)),
                ('eps', models.FloatField(blank=True, null=True)),
                ('bps', models.FloatField(blank=True, null=True)),
                ('volatility', models.FloatField(blank=True, null=True)),
                ('beta', models.FloatField(blank=True, null=True)),
                ('market_cap', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
    ]
