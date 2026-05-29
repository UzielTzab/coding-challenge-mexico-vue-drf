import json
import websockets
import logging
import traceback
import asyncio
from typing import Callable, Awaitable
from apps.exchanges.clients.base_client import BaseExchangeWebSocketClient
from apps.exchanges.normalizers.kraken_normalizer import KrakenNormalizer

logger = logging.getLogger(__name__)

class KrakenClient(BaseExchangeWebSocketClient):
    exchange_code = "kraken"
    websocket_url = "wss://ws.kraken.com/v2"

    def __init__(self, callback: Callable[[dict], Awaitable[None]] = None):
        super().__init__()
        self.normalizer = KrakenNormalizer()
        self.callback = callback

    async def connect(self):
        try:
            self.ws = await websockets.connect(self.websocket_url)
            self.is_connected = True
            logger.info(f"Connected to {self.exchange_code} websocket")
        except Exception as e:
            self.is_connected = False
            logger.error(f"Failed to connect to {self.exchange_code}: {e}")
            raise e

    async def subscribe(self):
        if not self.ws or not self.is_connected:
            return
        
        subscribe_message = {
            "method": "subscribe",
            "params": {
                "channel": "ticker",
                "symbol": ["BTC/USD"],
            },
        }
        await self.ws.send(json.dumps(subscribe_message))
        logger.info(f"Subscribed to {self.exchange_code} channels")

    async def listen(self):
        if not self.ws or not self.is_connected:
            return

        try:
            async for message in self.ws:
                data = json.loads(message)
                normalized = self.normalize_message(data)
                if normalized and self.callback:
                    await self.callback(normalized)
        except websockets.exceptions.ConnectionClosed:
            logger.warning(f"Connection closed for {self.exchange_code}")
        except Exception as e:
            logger.error(f"Error in {self.exchange_code} listen loop: {e}")
            logger.error(traceback.format_exc())
        finally:
            self.is_connected = False
            if self.ws:
                await self.ws.close()

    def normalize_message(self, raw_message: dict) -> dict:
        return self.normalizer.normalize(raw_message)
