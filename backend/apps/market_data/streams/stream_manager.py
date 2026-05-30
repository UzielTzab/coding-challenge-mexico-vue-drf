import asyncio
import logging
import json
from typing import Dict, Any
from asgiref.sync import sync_to_async
from django.utils import timezone
from apps.exchanges.models import Exchange
from apps.market_data.models import MarketSnapshot, OrderBookLevel
from apps.exchanges.clients.binance_client import BinanceClient
from apps.exchanges.clients.kraken_client import KrakenClient
from apps.exchanges.clients.bitfinex_client import BitfinexClient

logger = logging.getLogger(__name__)

class StreamManager:
    def __init__(self):
        self.clients = [
            BinanceClient(callback=self.handle_message),
            KrakenClient(callback=self.handle_message),
            BitfinexClient(callback=self.handle_message)
        ]
        self.exchanges_cache = {}

    @sync_to_async
    def get_exchange(self, code: str):
        if code not in self.exchanges_cache:
            exchange = Exchange.objects.filter(code=code).first()
            self.exchanges_cache[code] = exchange
        return self.exchanges_cache[code]

    @sync_to_async(thread_sensitive=False)
    def save_snapshot(self, exchange: Exchange, normalized_data: Dict[str, Any]):
        from django.db import transaction
        
        with transaction.atomic():
            best_bid = normalized_data["best_bid"]
            best_ask = normalized_data["best_ask"]
            
            # Optimización (Evitar miles de registros): Actualizar la fila en lugar de crear una nueva cada vez
            snapshot, created = MarketSnapshot.objects.update_or_create(
                exchange=exchange,
                symbol=normalized_data["symbol"],
                defaults={
                    'best_bid': best_bid,
                    'best_ask': best_ask,
                    'bid_volume': normalized_data["bid_volume"],
                    'ask_volume': normalized_data["ask_volume"],
                    'spread': best_ask - best_bid,
                    'latency_ms': normalized_data["latency_ms"],
                    'received_at': normalized_data["received_at"],
                    'raw_payload': normalized_data.get("raw_payload", {})
                }
            )

            # Update OrderBookLevel (solo nivel 0 para MVP, evitando bloat)
            OrderBookLevel.objects.update_or_create(
                snapshot=snapshot, side='ask', level_index=0,
                defaults={'price': best_ask, 'quantity': normalized_data["ask_volume"]}
            )
            OrderBookLevel.objects.update_or_create(
                snapshot=snapshot, side='bid', level_index=0,
                defaults={'price': best_bid, 'quantity': normalized_data["bid_volume"]}
            )

            # Hook for ArbitrageEngine (Fase BE-7)
            from apps.arbitrage.engine.arbitrage_engine import ArbitrageEngine
            ArbitrageEngine.process_snapshot(snapshot)

    async def handle_message(self, normalized_data: Dict[str, Any], raw_message: Dict[str, Any] = None):
        import time
        from channels.layers import get_channel_layer
        
        exchange_code = normalized_data.get("exchange_code")
        
        # Throttling logic to avoid huge DB latency (max 1 update per second per exchange)
        if not hasattr(self, 'last_updates'):
            self.last_updates = {}
            
        now = time.time()
        if exchange_code in self.last_updates and now - self.last_updates[exchange_code] < 1.0:
            return
        self.last_updates[exchange_code] = now
        
        exchange = await self.get_exchange(exchange_code)
        
        if exchange:
            # EMIT INSTANTLY: No database/network latency overhead!
            channel_layer = get_channel_layer()
            if channel_layer:
                await channel_layer.group_send(
                    "dashboard_updates",
                    {
                        "type": "dashboard_message",
                        "payload": {
                            "type": "market_update",
                            "exchange": exchange.code,
                            "symbol": normalized_data["symbol"],
                            "best_bid": str(normalized_data["best_bid"]),
                            "best_ask": str(normalized_data["best_ask"]),
                            "bid_volume": str(normalized_data["bid_volume"]),
                            "ask_volume": str(normalized_data["ask_volume"]),
                            "latency_ms": normalized_data.get("latency_ms", 0)
                        }
                    }
                )
            
            import datetime
            current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
            print(f"[{current_time}] EMITTING market_update -> [{exchange.code}] {normalized_data['symbol']} | Ask: {normalized_data['best_ask']} | Bid: {normalized_data['best_bid']}")

            # Fire and forget the DB save so Neon latency doesn't block the stream
            normalized_data_str = {k: str(v) for k, v in normalized_data.items()}
            normalized_data["raw_payload"] = normalized_data_str
            asyncio.create_task(self.save_snapshot(exchange, normalized_data))

    async def run_client(self, client):
        while True:
            try:
                await client.connect()
                await client.subscribe()
                await client.listen()
            except Exception as e:
                logger.error(f"Client {client.exchange_code} failed: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

    async def start(self):
        tasks = [self.run_client(client) for client in self.clients]
        await asyncio.gather(*tasks)
