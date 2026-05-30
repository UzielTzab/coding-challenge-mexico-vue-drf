import logging
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.market_data.models import MarketSnapshot
from apps.arbitrage.models import ArbitrageOpportunity, OpportunityCostBreakdown
from apps.arbitrage.engine.opportunity_detector import OpportunityDetector
from apps.arbitrage.calculators.net_profit_calculator import NetProfitCalculator

logger = logging.getLogger(__name__)

class ArbitrageEngine:
    @staticmethod
    def process_snapshot(new_snapshot: MarketSnapshot):
        """
        Main entry point for the arbitrage engine.
        Triggered when a new snapshot arrives.
        """
        # Fetch the latest snapshots of all OTHER active exchanges for the same symbol
        other_snapshots = MarketSnapshot.objects.filter(
            symbol=new_snapshot.symbol
        ).exclude(
            exchange=new_snapshot.exchange
        ).order_by('exchange_id', '-received_at').distinct('exchange_id')

        for other_snapshot in other_snapshots:
            # 1. Detect if gross spread exists
            opportunity_data = OpportunityDetector.detect(new_snapshot, other_snapshot)
            if not opportunity_data:
                continue
            
            # 2. Calculate true Net Profit considering fees and costs
            buy_snapshot = opportunity_data["buy_snapshot"]
            sell_snapshot = opportunity_data["sell_snapshot"]
            buy_price = opportunity_data["buy_price"]
            sell_price = opportunity_data["sell_price"]
            volume = opportunity_data["volume_available"]
            
            profit_data = NetProfitCalculator.calculate(
                buy_price=buy_price,
                sell_price=sell_price,
                quantity=volume,
                buy_exchange_id=buy_snapshot.exchange_id,
                sell_exchange_id=sell_snapshot.exchange_id
            )

            # 3. Decision Making
            is_profitable = profit_data["is_profitable"]
            from apps.system_logs.models import BotRuntimeState
            state = BotRuntimeState.objects.first()
            bot_running = state.is_running if state else False

            if is_profitable and not bot_running:
                status = 'discarded'
                reason = 'Bot está pausado (is_running=False)'
                is_profitable = False # Turn off so it doesn't execute
            else:
                status = 'profitable' if is_profitable else 'discarded'
                reason = 'Margen positivo después de comisiones' if is_profitable else 'Rentabilidad neta negativa tras comisiones y slippage'

            # 4. Save Opportunity to database
            opp = ArbitrageOpportunity.objects.create(
                symbol=new_snapshot.symbol,
                buy_exchange=buy_snapshot.exchange,
                sell_exchange=sell_snapshot.exchange,
                ask_price=buy_price,
                bid_price=sell_price,
                volume_available=volume,
                gross_spread=profit_data["gross_spread"],
                gross_spread_percent=profit_data["gross_spread_percent"],
                estimated_fees=profit_data["estimated_fees"],
                estimated_slippage=profit_data["slippage_usd"],
                withdrawal_cost=profit_data["withdrawal_fee_usd"],
                latency_penalty=profit_data["latency_penalty_usd"],
                net_profit=profit_data["net_profit"],
                net_profit_percent=profit_data["net_profit_percent"],
                status=status,
                decision_reason=reason,
                detected_at=timezone.now()
            )

            if is_profitable:
                OpportunityCostBreakdown.objects.create(
                    opportunity=opp,
                    buy_fee_usd=profit_data["buy_fee_usd"],
                    sell_fee_usd=profit_data["sell_fee_usd"],
                    withdrawal_fee_usd=profit_data["withdrawal_fee_usd"],
                    slippage_usd=profit_data["slippage_usd"],
                    latency_penalty_usd=profit_data["latency_penalty_usd"]
                )

            # 5. Emit Event via Channels
            ArbitrageEngine.emit_event(opp)

            # 6. Execute Simulation if Profitable
            if is_profitable:
                from apps.trading.engine.simulation_engine import SimulationEngine
                SimulationEngine.execute_opportunity(opp.id)

    @staticmethod
    def emit_event(opp: ArbitrageOpportunity):
        channel_layer = get_channel_layer()
        if not channel_layer:
            return

        payload = {
            "type": "opportunity_detected",
            "opportunity_id": opp.id,
            "symbol": opp.symbol,
            "buy_exchange": opp.buy_exchange.code,
            "sell_exchange": opp.sell_exchange.code,
            "net_profit": str(opp.net_profit),
            "gross_spread_percent": str(opp.gross_spread_percent),
            "status": opp.status
        }
        
        async_to_sync(channel_layer.group_send)(
            "dashboard_updates",
            {
                "type": "dashboard_message",
                "payload": payload
            }
        )
