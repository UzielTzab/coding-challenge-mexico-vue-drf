from decimal import Decimal
from typing import Dict, Any
from django.utils import timezone
from .base_normalizer import BaseNormalizer

class KrakenNormalizer(BaseNormalizer):
    def normalize(self, raw_message: Dict[str, Any]) -> Dict[str, Any]:
        if raw_message.get("channel") != "ticker" or "data" not in raw_message:
            return {}
        
        data = raw_message["data"][0]
        
        return {
            "exchange_code": "kraken",
            "symbol": data["symbol"],
            "best_bid": Decimal(str(data["bid"])),
            "bid_volume": Decimal(str(data["bid_qty"])),
            "best_ask": Decimal(str(data["ask"])),
            "ask_volume": Decimal(str(data["ask_qty"])),
            "exchange_timestamp": None,
            "received_at": timezone.now(),
            "latency_ms": 0,
        }
