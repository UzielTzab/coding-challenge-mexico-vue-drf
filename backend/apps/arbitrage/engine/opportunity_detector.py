from typing import Optional
from decimal import Decimal
from apps.market_data.models import MarketSnapshot

class OpportunityDetector:
    @staticmethod
    def detect(snapshot_a: MarketSnapshot, snapshot_b: MarketSnapshot) -> Optional[dict]:
        """
        Cross-checks two snapshots. Returns the best arbitrage direction if one exists.
        Returns None if no gross spread opportunity exists.
        """
        # Direction 1: Buy A, Sell B
        spread_1 = snapshot_b.best_bid - snapshot_a.best_ask

        # Direction 2: Buy B, Sell A
        spread_2 = snapshot_a.best_bid - snapshot_b.best_ask

        if spread_1 <= 0 and spread_2 <= 0:
            return None

        # Determine the most profitable direction
        if spread_1 > spread_2:
            buy_snapshot = snapshot_a
            sell_snapshot = snapshot_b
            gross_spread = spread_1
            buy_price = snapshot_a.best_ask
            sell_price = snapshot_b.best_bid
            volume = min(snapshot_a.ask_volume, snapshot_b.bid_volume)
        else:
            buy_snapshot = snapshot_b
            sell_snapshot = snapshot_a
            gross_spread = spread_2
            buy_price = snapshot_b.best_ask
            sell_price = snapshot_a.best_bid
            volume = min(snapshot_b.ask_volume, snapshot_a.bid_volume)

        # Cap the volume to 0.01 BTC maximum for safety and demo continuity
        volume = min(volume, Decimal('0.01'))

        return {
            "buy_snapshot": buy_snapshot,
            "sell_snapshot": sell_snapshot,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "volume_available": volume,
            "gross_spread": gross_spread
        }
