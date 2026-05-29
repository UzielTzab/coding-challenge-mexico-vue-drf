from django.db import models
from apps.exchanges.models import Exchange

class MarketSnapshot(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=30)
    best_bid = models.DecimalField(max_digits=20, decimal_places=8)
    best_ask = models.DecimalField(max_digits=20, decimal_places=8)
    bid_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    ask_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    spread = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    latency_ms = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField()

    def __str__(self):
        return f"{self.exchange.code} - {self.symbol} - {self.received_at}"
