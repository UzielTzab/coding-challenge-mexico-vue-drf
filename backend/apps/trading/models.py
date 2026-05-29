from django.db import models
from apps.arbitrage.models import ArbitrageOpportunity
from apps.exchanges.models import Exchange

class SimulatedTrade(models.Model):
    opportunity = models.OneToOneField(ArbitrageOpportunity, on_delete=models.SET_NULL, null=True, blank=True)
    symbol = models.CharField(max_length=30)
    buy_exchange = models.ForeignKey(Exchange, related_name='buy_trades', on_delete=models.CASCADE)
    sell_exchange = models.ForeignKey(Exchange, related_name='sell_trades', on_delete=models.CASCADE)
    quantity_btc = models.DecimalField(max_digits=20, decimal_places=8)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=8)
    sell_revenue = models.DecimalField(max_digits=20, decimal_places=8)
    total_fees = models.DecimalField(max_digits=20, decimal_places=8)
    slippage_cost = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    latency_cost = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    net_profit = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=30)
    executed_at = models.DateTimeField()

class TradeLeg(models.Model):
    trade = models.ForeignKey(SimulatedTrade, related_name='legs', on_delete=models.CASCADE)
    side = models.CharField(max_length=10) # buy/sell
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    status = models.CharField(max_length=30, default='executed')
    executed_at = models.DateTimeField()
