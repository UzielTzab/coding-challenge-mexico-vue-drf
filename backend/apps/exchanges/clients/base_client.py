import json
import asyncio
import websockets
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseExchangeWebSocketClient(ABC):
    exchange_code: str
    websocket_url: str

    def __init__(self):
        self.ws = None
        self.is_connected = False
    
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def subscribe(self):
        pass

    @abstractmethod
    async def listen(self):
        pass

    @abstractmethod
    def normalize_message(self, raw_message: dict) -> dict:
        pass
