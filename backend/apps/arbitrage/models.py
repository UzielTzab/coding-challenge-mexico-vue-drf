from django.db import models
from apps.exchanges.models import Exchange

class ArbitrageOpportunity(models.Model):
    buy_exchange = models.ForeignKey(Exchange, related_name='buy_opportunities', on_delete=models.CASCADE)
    sell_exchange = models.ForeignKey(Exchange, related_name='sell_opportunities', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=30)
    ask_price = models.DecimalField(max_digits=20, decimal_places=8)
    bid_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume_available = models.DecimalField(max_digits=20, decimal_places=8)
    gross_spread = models.DecimalField(max_digits=20, decimal_places=8)
    gross_spread_percent = models.DecimalField(max_digits=10, decimal_places=6)
    estimated_fees = models.DecimalField(max_digits=20, decimal_places=8)
    estimated_slippage = models.DecimalField(max_digits=20, decimal_places=8)
    withdrawal_cost = models.DecimalField(max_digits=20, decimal_places=8)
    latency_penalty = models.DecimalField(max_digits=20, decimal_places=8)
    net_profit = models.DecimalField(max_digits=20, decimal_places=8)
    net_profit_percent = models.DecimalField(max_digits=10, decimal_places=6)
    status = models.CharField(max_length=30)
    decision_reason = models.TextField(blank=True, null=True)
    detected_at = models.DateTimeField(db_index=True)

class OpportunityCostBreakdown(models.Model):
    opportunity = models.OneToOneField(ArbitrageOpportunity, on_delete=models.CASCADE, related_name='cost_breakdown')
    buy_fee_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    sell_fee_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    withdrawal_fee_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    slippage_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    latency_penalty_usd = models.DecimalField(max_digits=20, decimal_places=8, default=0)
