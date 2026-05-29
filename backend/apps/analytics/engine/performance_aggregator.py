import logging
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.trading.models import SimulatedTrade
from apps.analytics.models import PerformanceSnapshot
from apps.system_logs.models import SystemLog

logger = logging.getLogger(__name__)

class PerformanceAggregator:
    @staticmethod
    def calculate_global_snapshot():
        """
        Calculates the all-time performance of the bot and saves a PerformanceSnapshot.
        """
        trades = SimulatedTrade.objects.all()
        total_trades = trades.count()
        
        if total_trades == 0:
            return None

        profitable_trades = trades.filter(net_profit__gt=0).count()
        failed_trades = total_trades - profitable_trades

        win_rate = (Decimal(profitable_trades) / Decimal(total_trades)) * 100

        aggregate = trades.aggregate(total_pnl=Sum('net_profit'))
        total_pnl_usd = aggregate['total_pnl'] or Decimal('0.00')

        snapshot = PerformanceSnapshot.objects.create(
            total_pnl_usd=total_pnl_usd,
            total_trades=total_trades,
            profitable_trades=profitable_trades,
            failed_trades=failed_trades,
            win_rate_percent=win_rate,
            created_at=timezone.now()
        )

        logger.info(f"Performance snapshot created: PNL ${total_pnl_usd} | Win Rate {win_rate}%")
        SystemLog.objects.create(level="info", source="analytics", message=f"Snapshot actualizado: PNL ${total_pnl_usd:.2f}")

        PerformanceAggregator.emit_snapshot_event(snapshot)
        return snapshot

    @staticmethod
    def emit_snapshot_event(snapshot: PerformanceSnapshot):
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {
                    "type": "dashboard_message",
                    "payload": {
                        "type": "bot_status_changed",
                        "total_pnl_usd": str(snapshot.total_pnl_usd),
                        "total_trades": snapshot.total_trades,
                        "profitable_trades": snapshot.profitable_trades,
                        "win_rate_percent": str(snapshot.win_rate_percent)
                    }
                }
            )
