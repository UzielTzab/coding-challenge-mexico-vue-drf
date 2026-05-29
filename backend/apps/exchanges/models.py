from django.db import models

class Exchange(models.Model):
    name = models.CharField(max_length=80, unique=True)
    code = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    websocket_url = models.URLField(blank=True, null=True)
    trading_fee_percent = models.DecimalField(max_digits=8, decimal_places=5, default=0.10000)
    withdrawal_fee_btc = models.DecimalField(max_digits=18, decimal_places=8, default=0.00050000)

    def __str__(self):
        return self.name
