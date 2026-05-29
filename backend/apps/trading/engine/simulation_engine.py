import logging
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.arbitrage.models import ArbitrageOpportunity
from apps.trading.models import SimulatedTrade, TradeLeg
from apps.wallets.models import Wallet, WalletMovement
from apps.system_logs.models import SystemLog

logger = logging.getLogger(__name__)

class SimulationEngine:
    @staticmethod
    def execute_opportunity(opportunity_id: int):
        with transaction.atomic():
            opp = ArbitrageOpportunity.objects.select_for_update().get(id=opportunity_id)
            if opp.status != 'profitable':
                return

            buy_wallet = Wallet.objects.select_for_update().filter(exchange=opp.buy_exchange).first()
            sell_wallet = Wallet.objects.select_for_update().filter(exchange=opp.sell_exchange).first()

            if not buy_wallet or not sell_wallet:
                opp.status = 'failed'
                opp.decision_reason = 'Wallets no encontradas'
                opp.save()
                return

            buy_price = opp.ask_price
            sell_price = opp.bid_price
            volume = opp.volume_available
            
            # Required balances
            # Check for partial execution
            max_volume_usdt = buy_wallet.usdt_available / buy_price if buy_price > 0 else Decimal('0')
            max_volume_btc = sell_wallet.btc_available
            
            actual_volume = min(volume, max_volume_usdt, max_volume_btc)

            if actual_volume <= Decimal('0.00000001'):
                opp.status = 'failed'
                opp.decision_reason = 'Fondos insuficientes en Wallets'
                opp.save()
                return

            # Update opportunity if partial execution
            if actual_volume < volume:
                opp.status = 'partially_executed'
                opp.volume_available = actual_volume
                
                scale = actual_volume / volume
                opp.gross_spread = opp.gross_spread * scale
                opp.estimated_fees = opp.estimated_fees * scale
                opp.net_profit = opp.net_profit * scale
            else:
                opp.status = 'executed'

            opp.save()

            # Execute Wallet Movements
            # 1. Buy Exchange: Spend USDT, Get BTC
            actual_buy_cost_usdt = actual_volume * buy_price
            fee_buy = opp.estimated_fees / Decimal('2') # simplified scaling

            SimulationEngine._apply_movement(buy_wallet, 'buy_trade', 'USDT', -actual_buy_cost_usdt, opp.id)
            SimulationEngine._apply_movement(buy_wallet, 'buy_trade', 'BTC', actual_volume, opp.id)

            # 2. Sell Exchange: Spend BTC, Get USDT
            actual_sell_revenue_usdt = actual_volume * sell_price
            SimulationEngine._apply_movement(sell_wallet, 'sell_trade', 'BTC', -actual_volume, opp.id)
            SimulationEngine._apply_movement(sell_wallet, 'sell_trade', 'USDT', actual_sell_revenue_usdt, opp.id)

            # Record the Trade
            trade = SimulatedTrade.objects.create(
                opportunity=opp,
                symbol=opp.symbol,
                buy_exchange=opp.buy_exchange,
                sell_exchange=opp.sell_exchange,
                quantity_btc=actual_volume,
                buy_cost=actual_buy_cost_usdt,
                sell_revenue=actual_sell_revenue_usdt,
                total_fees=opp.estimated_fees,
                slippage_cost=opp.estimated_slippage,
                latency_cost=opp.latency_penalty,
                net_profit=opp.net_profit,
                status=opp.status,
                executed_at=timezone.now()
            )

            # Record Legs
            TradeLeg.objects.create(trade=trade, side='buy', exchange=opp.buy_exchange, price=buy_price, quantity=actual_volume, fee=fee_buy, executed_at=trade.executed_at)
            TradeLeg.objects.create(trade=trade, side='sell', exchange=opp.sell_exchange, price=sell_price, quantity=actual_volume, fee=fee_buy, executed_at=trade.executed_at)

            # Logs
            SystemLog.objects.create(level="success", source="trading", message=f"Trade simulado ejecutado: {actual_volume} BTC ({opp.buy_exchange.code} -> {opp.sell_exchange.code}) | PNL: ${opp.net_profit:.2f}")

            # Emit Events
            SimulationEngine.emit_trade_event(trade)
            SimulationEngine.emit_wallet_event(buy_wallet)
            SimulationEngine.emit_wallet_event(sell_wallet)

            # Analytics (Fase BE-9)
            from apps.analytics.engine.performance_aggregator import PerformanceAggregator
            PerformanceAggregator.calculate_global_snapshot()

    @staticmethod
    def _apply_movement(wallet: Wallet, m_type: str, asset: str, amount: Decimal, ref_id: int):
        if asset == 'USDT':
            balance_before = wallet.usdt_available
            wallet.usdt_available += amount
            balance_after = wallet.usdt_available
        else:
            balance_before = wallet.btc_available
            wallet.btc_available += amount
            balance_after = wallet.btc_available
            
        wallet.save()

        WalletMovement.objects.create(
            wallet=wallet,
            movement_type=m_type,
            asset=asset,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            reference_type='arbitrage_opportunity',
            reference_id=str(ref_id)
        )

    @staticmethod
    def emit_trade_event(trade: SimulatedTrade):
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {
                    "type": "dashboard_message",
                    "payload": {
                        "type": "trade_simulated",
                        "trade_id": trade.id,
                        "quantity_btc": str(trade.quantity_btc),
                        "net_profit": str(trade.net_profit),
                        "status": trade.status
                    }
                }
            )

    @staticmethod
    def emit_wallet_event(wallet: Wallet):
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {
                    "type": "dashboard_message",
                    "payload": {
                        "type": "wallet_updated",
                        "exchange": wallet.exchange.code,
                        "btc_available": str(wallet.btc_available),
                        "usdt_available": str(wallet.usdt_available)
                    }
                }
            )
