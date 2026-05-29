import random
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from apps.exchanges.models import Exchange
from apps.market_data.models import MarketSnapshot
from apps.arbitrage.models import ArbitrageOpportunity
from apps.trading.models import SimulatedTrade
from apps.wallets.models import Wallet, WalletMovement
from apps.system_logs.models import SystemLog

class Command(BaseCommand):
    help = 'Seeda la base de datos con datos simulados (Fase 2)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Borrando datos anteriores...")
        Exchange.objects.all().delete()
        SystemLog.objects.all().delete()
        
        now = timezone.now()

        # 1. Exchanges
        self.stdout.write("Creando Exchanges...")
        binance = Exchange.objects.create(name="Binance", code="binance", trading_fee_percent=Decimal('0.10'), withdrawal_fee_btc=Decimal('0.0005'))
        kraken = Exchange.objects.create(name="Kraken", code="kraken", trading_fee_percent=Decimal('0.16'), withdrawal_fee_btc=Decimal('0.0005'))
        coinbase = Exchange.objects.create(name="Coinbase", code="coinbase", trading_fee_percent=Decimal('0.20'), withdrawal_fee_btc=Decimal('0.0005'))
        
        # 2. Wallets
        self.stdout.write("Creando Wallets...")
        Wallet.objects.create(exchange=binance, btc_available=Decimal('1.2'), usdt_available=Decimal('15000'))
        Wallet.objects.create(exchange=kraken, btc_available=Decimal('1.0'), usdt_available=Decimal('12000'))
        Wallet.objects.create(exchange=coinbase, btc_available=Decimal('0.8'), usdt_available=Decimal('9000'))

        # 3. Market Snapshots
        self.stdout.write("Creando Market Snapshots...")
        symbol = "BTC/USDT"
        
        MarketSnapshot.objects.create(
            exchange=binance, symbol=symbol,
            best_ask=Decimal('69657.20'), best_bid=Decimal('69642.10'),
            ask_volume=Decimal('2.5'), bid_volume=Decimal('3.1'),
            received_at=now
        )
        MarketSnapshot.objects.create(
            exchange=kraken, symbol=symbol,
            best_ask=Decimal('69612.70'), best_bid=Decimal('69598.40'),
            ask_volume=Decimal('1.8'), bid_volume=Decimal('2.2'),
            received_at=now
        )
        MarketSnapshot.objects.create(
            exchange=coinbase, symbol=symbol,
            best_ask=Decimal('69648.30'), best_bid=Decimal('69631.80'),
            ask_volume=Decimal('1.5'), bid_volume=Decimal('1.9'),
            received_at=now
        )

        # 4. Opportunities (20)
        self.stdout.write("Creando Oportunidades...")
        exchanges = [binance, kraken, coinbase]
        opportunities = []
        for i in range(20):
            buy_ex = random.choice(exchanges)
            sell_ex = random.choice([e for e in exchanges if e != buy_ex])
            
            # Simulated prices
            ask_price = Decimal(random.uniform(69000, 69500)).quantize(Decimal('0.01'))
            bid_price = ask_price + Decimal(random.uniform(10, 100)).quantize(Decimal('0.01'))
            volume = Decimal(random.uniform(0.1, 1.5)).quantize(Decimal('0.0001'))
            gross = (bid_price - ask_price) * volume
            net = gross - Decimal('15.00') # simulated costs
            
            status = 'executed' if i < 10 else random.choice(['detected', 'profitable', 'discarded', 'failed'])
            reason = "Condiciones favorables" if status in ['profitable', 'executed'] else "Spread insuficiente"
            
            opp = ArbitrageOpportunity.objects.create(
                buy_exchange=buy_ex, sell_exchange=sell_ex, symbol=symbol,
                ask_price=ask_price, bid_price=bid_price, volume_available=volume,
                gross_spread=gross, net_profit=net, net_profit_percent=(net/(ask_price*volume))*100,
                status=status, decision_reason=reason,
                detected_at=now - timedelta(minutes=random.randint(1, 60))
            )
            if status == 'executed':
                opportunities.append(opp)

        # 5. Simulated Trades
        self.stdout.write("Creando Simulated Trades...")
        num_trades = min(10, len(opportunities))
        for i in range(num_trades):
            opp = opportunities[i]
            buy_ex = opp.buy_exchange
            sell_ex = opp.sell_exchange
            
            qty = Decimal(random.uniform(0.05, 0.5)).quantize(Decimal('0.0001'))
            buy_p = Decimal(random.uniform(69000, 69500)).quantize(Decimal('0.01'))
            sell_p = buy_p + Decimal(random.uniform(20, 80)).quantize(Decimal('0.01'))
            
            net_prof = (sell_p - buy_p) * qty - Decimal('10')
            
            SimulatedTrade.objects.create(
                opportunity=opp, symbol=symbol,
                buy_exchange=buy_ex, sell_exchange=sell_ex,
                quantity_btc=qty, buy_price=buy_p, sell_price=sell_p,
                buy_cost=buy_p * qty, sell_revenue=sell_p * qty,
                total_fees=Decimal('5'), net_profit=net_prof,
                status=random.choice(['executed', 'partially_executed']),
                executed_at=now - timedelta(minutes=random.randint(1, 60))
            )

        # 6. System Logs
        self.stdout.write("Creando System Logs...")
        for msg in ["Conectado a Binance WS", "Conectado a Kraken WS", "Simulación completada", "Oportunidad detectada"]:
            SystemLog.objects.create(
                level=random.choice(["info", "success"]),
                source="system",
                message=msg
            )
        
        self.stdout.write(self.style.SUCCESS('¡Seed data completado exitosamente!'))
