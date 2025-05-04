from django.db import models

class StockOrder(models.Model):
    stock_code = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('buy', '매수'), ('sell', '매도')])
    order_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name} ({self.stock_code}) - {self.quantity}주"
