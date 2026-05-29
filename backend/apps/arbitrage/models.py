from django.db import models
from apps.exchanges.models import Exchange

class ArbitrageOpportunity(models.Model):
    STATUS_CHOICES = [
        ("detected", "Detectada"),
        ("profitable", "Rentable"),
        ("discarded", "Descartada"),
        ("executed", "Ejecutada"),
        ("failed", "Fallida"),
    ]

    buy_exchange = models.ForeignKey(Exchange, related_name="buy_opportunities", on_delete=models.CASCADE)
    sell_exchange = models.ForeignKey(Exchange, related_name="sell_opportunities", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=30)
    
    ask_price = models.DecimalField(max_digits=20, decimal_places=8)
    bid_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume_available = models.DecimalField(max_digits=20, decimal_places=8)
    
    gross_spread = models.DecimalField(max_digits=20, decimal_places=8)
    estimated_fees = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    estimated_slippage = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    latency_penalty = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    net_profit = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    net_profit_percent = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="detected")
    detected_at = models.DateTimeField()
    decision_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.buy_exchange.code} -> {self.sell_exchange.code} | {self.net_profit_percent}%"
