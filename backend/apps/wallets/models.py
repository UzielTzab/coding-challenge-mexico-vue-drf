from django.db import models
from apps.exchanges.models import Exchange

class Wallet(models.Model):
    exchange = models.OneToOneField(Exchange, on_delete=models.CASCADE)
    btc_available = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    usdt_available = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    btc_locked = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    usdt_locked = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_value_usd = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    updated_at = models.DateTimeField(auto_now=True)

class WalletMovement(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='movements', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=30)
    asset = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    balance_before = models.DecimalField(max_digits=24, decimal_places=8)
    balance_after = models.DecimalField(max_digits=24, decimal_places=8)
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
