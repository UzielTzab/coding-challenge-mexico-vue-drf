from django.db import models

class Exchange(models.Model):
    name = models.CharField(max_length=80)
    code = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    websocket_url = models.URLField(blank=True, null=True)
    rest_url = models.URLField(blank=True, null=True)
    latency_ms = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='disconnected')

    def __str__(self):
        return self.name

class ExchangeFeeProfile(models.Model):
    exchange = models.OneToOneField(Exchange, on_delete=models.CASCADE, related_name='fee_profile')
    trading_fee_percent = models.DecimalField(max_digits=8, decimal_places=5, default=0.10000)
    withdrawal_fee_btc = models.DecimalField(max_digits=18, decimal_places=8, default=0.00050000)
