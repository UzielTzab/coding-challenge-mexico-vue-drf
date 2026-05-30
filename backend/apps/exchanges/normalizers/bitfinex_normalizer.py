from decimal import Decimal
from typing import Dict, Any, List
from django.utils import timezone
from .base_normalizer import BaseNormalizer

class BitfinexNormalizer(BaseNormalizer):
    def normalize(self, raw_message: Any) -> Dict[str, Any]:
        # Bitfinex sends an array format:
        # [ CHANNEL_ID, [ BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW ] ]
        # It also sends events like {"event": "info", ...} or {"event": "subscribed", ...} which are dicts.
        
        # If it's a dict (e.g. heartbeat or event info), ignore it
        if isinstance(raw_message, dict):
            return {}

        # If it's an array but length < 2, ignore
        if not isinstance(raw_message, list) or len(raw_message) < 2:
            return {}

        # Heartbeat arrays like [ CHANNEL_ID, "hb" ]
        if raw_message[1] == "hb":
            return {}

        data = raw_message[1]
        
        # Make sure data is a list of numbers
        if not isinstance(data, list) or len(data) < 4:
            return {}

        # Extract according to Bitfinex v2 ticker spec
        best_bid = data[0]
        bid_size = data[1]
        best_ask = data[2]
        ask_size = data[3]

        return {
            "exchange_code": "bitfinex",
            "symbol": "BTC/USDT", # Normalizing tBTCUSD to BTC/USDT as requested
            "best_bid": Decimal(str(best_bid)),
            "bid_volume": Decimal(str(bid_size)),
            "best_ask": Decimal(str(best_ask)),
            "ask_volume": Decimal(str(ask_size)),
            "exchange_timestamp": None,
            "received_at": timezone.now(),
            "latency_ms": 0,
        }
