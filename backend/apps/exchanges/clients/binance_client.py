import json
import websockets
import logging
import traceback
import asyncio
from typing import Callable, Awaitable
from apps.exchanges.clients.base_client import BaseExchangeWebSocketClient
from apps.exchanges.normalizers.binance_normalizer import BinanceNormalizer

logger = logging.getLogger(__name__)

class BinanceClient(BaseExchangeWebSocketClient):
    exchange_code = "binance"
    websocket_url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"

    def __init__(self, callback: Callable[[dict], Awaitable[None]] = None):
        super().__init__()
        self.normalizer = BinanceNormalizer()
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
        pass

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
