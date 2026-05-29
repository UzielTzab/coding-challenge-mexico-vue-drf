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

logger = logging.getLogger(__name__)

class StreamManager:
    def __init__(self):
        self.clients = [
            BinanceClient(callback=self.handle_message),
            KrakenClient(callback=self.handle_message)
        ]
        self.exchanges_cache = {}

    @sync_to_async
    def get_exchange(self, code: str):
        if code not in self.exchanges_cache:
            exchange = Exchange.objects.filter(code=code).first()
            self.exchanges_cache[code] = exchange
        return self.exchanges_cache[code]

    @sync_to_async
    def save_snapshot(self, exchange: Exchange, normalized_data: Dict[str, Any]):
        best_bid = normalized_data["best_bid"]
        best_ask = normalized_data["best_ask"]
        spread = best_ask - best_bid

        snapshot = MarketSnapshot.objects.create(
            exchange=exchange,
            symbol=normalized_data["symbol"],
            best_bid=best_bid,
            best_ask=best_ask,
            bid_volume=normalized_data["bid_volume"],
            ask_volume=normalized_data["ask_volume"],
            spread=spread,
            latency_ms=normalized_data["latency_ms"],
            received_at=normalized_data["received_at"],
            raw_payload=normalized_data.get("raw_payload", {})
        )

        OrderBookLevel.objects.create(
            snapshot=snapshot, side='ask', price=best_ask, quantity=normalized_data["ask_volume"], level_index=0
        )
        OrderBookLevel.objects.create(
            snapshot=snapshot, side='bid', price=best_bid, quantity=normalized_data["bid_volume"], level_index=0
        )

        # Hook for ArbitrageEngine (Fase BE-7)
        from apps.arbitrage.engine.arbitrage_engine import ArbitrageEngine
        ArbitrageEngine.process_snapshot(snapshot)

        # Emit WebSocket Event
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {
                    "type": "dashboard_message",
                    "payload": {
                        "type": "market_update",
                        "exchange": exchange.code,
                        "symbol": snapshot.symbol,
                        "best_bid": str(snapshot.best_bid),
                        "best_ask": str(snapshot.best_ask),
                        "bid_volume": str(snapshot.bid_volume),
                        "ask_volume": str(snapshot.ask_volume),
                        "latency_ms": snapshot.latency_ms
                    }
                }
            )

        print(f"[{exchange.code}] {snapshot.symbol} | Ask: {snapshot.best_ask} | Bid: {snapshot.best_bid} | Vol: {snapshot.ask_volume}/{snapshot.bid_volume}")

    async def handle_message(self, normalized_data: Dict[str, Any], raw_message: Dict[str, Any] = None):
        exchange_code = normalized_data.get("exchange_code")
        exchange = await self.get_exchange(exchange_code)
        
        if exchange:
            # Avoid Decimal/datetime JSON serialization errors
            normalized_data_str = {k: str(v) for k, v in normalized_data.items()}
            normalized_data["raw_payload"] = normalized_data_str
            await self.save_snapshot(exchange, normalized_data)

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
