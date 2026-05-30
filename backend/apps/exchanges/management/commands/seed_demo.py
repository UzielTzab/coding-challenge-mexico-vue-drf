import random
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from apps.exchanges.models import Exchange, ExchangeFeeProfile
from apps.market_data.models import MarketSnapshot, OrderBookLevel
from apps.arbitrage.models import ArbitrageOpportunity, OpportunityCostBreakdown
from apps.trading.models import SimulatedTrade, TradeLeg
from apps.wallets.models import Wallet, WalletMovement
from apps.system_logs.models import SystemLog, BotRuntimeState
from apps.analytics.models import PerformanceSnapshot

class Command(BaseCommand):
    help = 'Seeda la base de datos con datos simulados (Arquitectura V2)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Borrando datos anteriores...")
        Exchange.objects.all().delete()
        SystemLog.objects.all().delete()
        BotRuntimeState.objects.all().delete()
        PerformanceSnapshot.objects.all().delete()
        
        now = timezone.now()

        # 1. Exchanges and Fee Profiles
        self.stdout.write("Creando Exchanges y Fees...")
        binance = Exchange.objects.create(name="Binance", code="binance")
        ExchangeFeeProfile.objects.create(exchange=binance, trading_fee_percent=Decimal('0.10'), withdrawal_fee_btc=Decimal('0.0005'))
        
        kraken = Exchange.objects.create(name="Kraken", code="kraken")
        ExchangeFeeProfile.objects.create(exchange=kraken, trading_fee_percent=Decimal('0.16'), withdrawal_fee_btc=Decimal('0.0005'))
        
        coinbase = Exchange.objects.create(name="Coinbase", code="coinbase")
        ExchangeFeeProfile.objects.create(exchange=coinbase, trading_fee_percent=Decimal('0.20'), withdrawal_fee_btc=Decimal('0.0005'))
        
        bitfinex = Exchange.objects.create(name="Bitfinex", code="bitfinex")
        ExchangeFeeProfile.objects.create(exchange=bitfinex, trading_fee_percent=Decimal('0.20'), withdrawal_fee_btc=Decimal('0.0004'))
        
        # 2. Wallets
        self.stdout.write("Creando Wallets...")
        Wallet.objects.create(exchange=binance, btc_available=Decimal('1.2'), usdt_available=Decimal('15000'))
        Wallet.objects.create(exchange=kraken, btc_available=Decimal('1.0'), usdt_available=Decimal('12000'))
        Wallet.objects.create(exchange=coinbase, btc_available=Decimal('0.8'), usdt_available=Decimal('9000'))
        Wallet.objects.create(exchange=bitfinex, btc_available=Decimal('0.5'), usdt_available=Decimal('5000'))

        # 3. Market Snapshots and OrderBook Levels
        self.stdout.write("Creando Market Snapshots...")
        symbol = "BTC/USDT"
        
        snap_binance = MarketSnapshot.objects.create(
            exchange=binance, symbol=symbol,
            best_ask=Decimal('69657.20'), best_bid=Decimal('69642.10'),
            ask_volume=Decimal('2.5'), bid_volume=Decimal('3.1'),
            received_at=now
        )
        OrderBookLevel.objects.create(snapshot=snap_binance, side='ask', price=Decimal('69657.20'), quantity=Decimal('2.5'), level_index=0)
        OrderBookLevel.objects.create(snapshot=snap_binance, side='bid', price=Decimal('69642.10'), quantity=Decimal('3.1'), level_index=0)

        snap_kraken = MarketSnapshot.objects.create(
            exchange=kraken, symbol=symbol,
            best_ask=Decimal('69612.70'), best_bid=Decimal('69598.40'),
            ask_volume=Decimal('1.8'), bid_volume=Decimal('2.2'),
            received_at=now
        )
        OrderBookLevel.objects.create(snapshot=snap_kraken, side='ask', price=Decimal('69612.70'), quantity=Decimal('1.8'), level_index=0)
        OrderBookLevel.objects.create(snapshot=snap_kraken, side='bid', price=Decimal('69598.40'), quantity=Decimal('2.2'), level_index=0)

        snap_coinbase = MarketSnapshot.objects.create(
            exchange=coinbase, symbol=symbol,
            best_ask=Decimal('69648.30'), best_bid=Decimal('69631.80'),
            ask_volume=Decimal('1.5'), bid_volume=Decimal('1.9'),
            received_at=now
        )
        OrderBookLevel.objects.create(snapshot=snap_coinbase, side='ask', price=Decimal('69648.30'), quantity=Decimal('1.5'), level_index=0)
        OrderBookLevel.objects.create(snapshot=snap_coinbase, side='bid', price=Decimal('69631.80'), quantity=Decimal('1.9'), level_index=0)

        # 4. Opportunities
        self.stdout.write("Creando Oportunidades y CostBreakdowns...")
        exchanges = [binance, kraken, coinbase, bitfinex]
        opportunities = []
        for i in range(20):
            buy_ex = random.choice(exchanges)
            sell_ex = random.choice([e for e in exchanges if e != buy_ex])
            
            ask_price = Decimal(random.uniform(69000, 69500)).quantize(Decimal('0.01'))
            bid_price = ask_price + Decimal(random.uniform(10, 100)).quantize(Decimal('0.01'))
            volume = Decimal(random.uniform(0.1, 1.5)).quantize(Decimal('0.0001'))
            gross = (bid_price - ask_price) * volume
            fees = Decimal('10.00')
            slip = Decimal('2.00')
            with_c = Decimal('3.00')
            lat_p = Decimal('0.00')
            net = gross - fees - slip - with_c - lat_p
            
            status = 'executed' if i < 10 else random.choice(['detected', 'profitable', 'discarded', 'failed'])
            reason = "Condiciones favorables" if status in ['profitable', 'executed'] else "Spread insuficiente"
            
            opp = ArbitrageOpportunity.objects.create(
                buy_exchange=buy_ex, sell_exchange=sell_ex, symbol=symbol,
                ask_price=ask_price, bid_price=bid_price, volume_available=volume,
                gross_spread=gross, gross_spread_percent=(gross/(ask_price*volume))*100,
                estimated_fees=fees, estimated_slippage=slip, withdrawal_cost=with_c, latency_penalty=lat_p,
                net_profit=net, net_profit_percent=(net/(ask_price*volume))*100,
                status=status, decision_reason=reason,
                detected_at=now - timedelta(minutes=random.randint(1, 60))
            )
            OpportunityCostBreakdown.objects.create(
                opportunity=opp, buy_fee_usd=Decimal('4.00'), sell_fee_usd=Decimal('6.00'),
                withdrawal_fee_usd=with_c, slippage_usd=slip, latency_penalty_usd=lat_p
            )

            if status == 'executed':
                opportunities.append(opp)

        # 5. Simulated Trades & TradeLegs
        self.stdout.write("Creando Simulated Trades y TradeLegs...")
        num_trades = min(10, len(opportunities))
        for i in range(num_trades):
            opp = opportunities[i]
            buy_ex = opp.buy_exchange
            sell_ex = opp.sell_exchange
            
            qty = Decimal(random.uniform(0.05, 0.5)).quantize(Decimal('0.0001'))
            buy_p = Decimal(random.uniform(69000, 69500)).quantize(Decimal('0.01'))
            sell_p = buy_p + Decimal(random.uniform(20, 80)).quantize(Decimal('0.01'))
            
            buy_cost = buy_p * qty
            sell_revenue = sell_p * qty
            net_prof = sell_revenue - buy_cost - Decimal('10')
            
            trade = SimulatedTrade.objects.create(
                opportunity=opp, symbol=symbol,
                buy_exchange=buy_ex, sell_exchange=sell_ex,
                quantity_btc=qty, buy_cost=buy_cost, sell_revenue=sell_revenue,
                total_fees=Decimal('5'), slippage_cost=Decimal('2'), latency_cost=Decimal('0'),
                net_profit=net_prof,
                status=random.choice(['executed', 'partially_executed']),
                executed_at=now - timedelta(minutes=random.randint(1, 60))
            )
            
            TradeLeg.objects.create(trade=trade, side='buy', exchange=buy_ex, price=buy_p, quantity=qty, fee=Decimal('2.5'), executed_at=trade.executed_at)
            TradeLeg.objects.create(trade=trade, side='sell', exchange=sell_ex, price=sell_p, quantity=qty, fee=Decimal('2.5'), executed_at=trade.executed_at)

        # 6. System Logs, BotRuntimeState & PerformanceSnapshot
        self.stdout.write("Creando System Logs & Analytics...")
        BotRuntimeState.objects.create(is_running=True, mode='simulation', circuit_breaker_active=False)
        PerformanceSnapshot.objects.create(total_pnl_usd=Decimal('450.25'), total_trades=10, profitable_trades=8, failed_trades=2, win_rate_percent=Decimal('80.00'))

        for msg in ["Conectado a Binance WS", "Conectado a Kraken WS", "Simulación completada", "Oportunidad detectada"]:
            SystemLog.objects.create(
                level=random.choice(["info", "success"]),
                source="system",
                message=msg
            )
        
        self.stdout.write(self.style.SUCCESS('¡Seed data completado exitosamente (V2)!'))
