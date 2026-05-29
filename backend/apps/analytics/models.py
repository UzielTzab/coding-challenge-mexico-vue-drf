from django.db import models

class PerformanceSnapshot(models.Model):
    total_pnl_usd = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    total_trades = models.PositiveIntegerField(default=0)
    profitable_trades = models.PositiveIntegerField(default=0)
    discarded_opportunities = models.PositiveIntegerField(default=0)
    failed_trades = models.PositiveIntegerField(default=0)
    total_fees_usd = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    average_execution_time_ms = models.PositiveIntegerField(default=0)
    win_rate_percent = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
