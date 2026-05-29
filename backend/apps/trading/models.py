from django.db import models
from apps.exchanges.models import Exchange
from apps.arbitrage.models import ArbitrageOpportunity

class SimulatedTrade(models.Model):
    STATUS_CHOICES = [
        ("executed", "Ejecutada"),
        ("partially_executed", "Ejecutada parcialmente"),
        ("failed", "Fallida"),
        ("discarded", "Descartada"),
    ]

    opportunity = models.OneToOneField(ArbitrageOpportunity, on_delete=models.SET_NULL, null=True, blank=True)
    symbol = models.CharField(max_length=30)
    
    buy_exchange = models.ForeignKey(Exchange, related_name="buy_trades", on_delete=models.CASCADE)
    sell_exchange = models.ForeignKey(Exchange, related_name="sell_trades", on_delete=models.CASCADE)
    
    quantity_btc = models.DecimalField(max_digits=20, decimal_places=8)
    
    buy_price = models.DecimalField(max_digits=20, decimal_places=8)
    sell_price = models.DecimalField(max_digits=20, decimal_places=8)
    
    buy_cost = models.DecimalField(max_digits=20, decimal_places=8)
    sell_revenue = models.DecimalField(max_digits=20, decimal_places=8)
    
    total_fees = models.DecimalField(max_digits=20, decimal_places=8)
    slippage_cost = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    latency_cost = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    net_profit = models.DecimalField(max_digits=20, decimal_places=8)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    executed_at = models.DateTimeField()

    def __str__(self):
        return f"Trade {self.id} - {self.net_profit} USD"
