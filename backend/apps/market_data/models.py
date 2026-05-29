from django.db import models
from apps.exchanges.models import Exchange

class MarketSnapshot(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=30)
    best_bid = models.DecimalField(max_digits=20, decimal_places=8)
    best_ask = models.DecimalField(max_digits=20, decimal_places=8)
    bid_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    ask_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    spread = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    latency_ms = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(db_index=True)
    raw_payload = models.JSONField(blank=True, null=True)

class OrderBookLevel(models.Model):
    snapshot = models.ForeignKey(MarketSnapshot, on_delete=models.CASCADE, related_name='levels')
    side = models.CharField(max_length=10) # buy/sell
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    level_index = models.PositiveIntegerField(default=0)
