from decimal import Decimal
from typing import Dict, Any
from django.utils import timezone
from .base_normalizer import BaseNormalizer

class BinanceNormalizer(BaseNormalizer):
    def normalize(self, raw_message: Dict[str, Any]) -> Dict[str, Any]:
        if 's' not in raw_message:
            return {}

        symbol = raw_message['s']
        normalized_symbol = "BTC/USDT" if symbol == "BTCUSDT" else symbol

        return {
            "exchange_code": "binance",
            "symbol": normalized_symbol,
            "best_bid": Decimal(raw_message["b"]),
            "bid_volume": Decimal(raw_message["B"]),
            "best_ask": Decimal(raw_message["a"]),
            "ask_volume": Decimal(raw_message["A"]),
            "exchange_timestamp": None,
            "received_at": timezone.now(),
            "latency_ms": 0,
        }
