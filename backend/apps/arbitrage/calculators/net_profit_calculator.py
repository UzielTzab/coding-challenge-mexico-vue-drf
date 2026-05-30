from decimal import Decimal
from apps.exchanges.models import ExchangeFeeProfile
from typing import Dict, Any

class NetProfitCalculator:
    @staticmethod
    def calculate(buy_price: Decimal, sell_price: Decimal, quantity: Decimal, 
                  buy_exchange_id: int, sell_exchange_id: int) -> Dict[str, Any]:
        """
        Calculates all costs and profitability for an arbitrage opportunity.
        """
        # Get fee profiles
        buy_profile = ExchangeFeeProfile.objects.filter(exchange_id=buy_exchange_id).first()
        sell_profile = ExchangeFeeProfile.objects.filter(exchange_id=sell_exchange_id).first()
        
        # Default fallback fees if no profile exists
        buy_fee_pct = buy_profile.trading_fee_percent if buy_profile else Decimal('0.10')
        sell_fee_pct = sell_profile.trading_fee_percent if sell_profile else Decimal('0.10')
        withdrawal_fee_btc = buy_profile.withdrawal_fee_btc if buy_profile else Decimal('0.0005')

        # Raw values
        buy_cost = buy_price * quantity
        sell_revenue = sell_price * quantity
        gross_spread = sell_revenue - buy_cost
        
        # Fees in USD
        buy_fee_usd = buy_cost * (buy_fee_pct / Decimal('100'))
        sell_fee_usd = sell_revenue * (sell_fee_pct / Decimal('100'))
        withdrawal_fee_usd = withdrawal_fee_btc * buy_price  # Approx cost in USD
        
        # Fixed assumed slippage and latency (Could be dynamic later)
        slippage_usd = Decimal('0.00')  # Flat assumed slippage
        latency_penalty_usd = Decimal('0.00')

        total_costs = buy_fee_usd + sell_fee_usd + withdrawal_fee_usd + slippage_usd + latency_penalty_usd
        net_profit = gross_spread - total_costs
        
        # Profit percentage based on investment (buy_cost)
        net_profit_percent = (net_profit / buy_cost) * 100 if buy_cost > 0 else Decimal('0')
        gross_spread_percent = (gross_spread / buy_cost) * 100 if buy_cost > 0 else Decimal('0')

        return {
            "gross_spread": gross_spread,
            "gross_spread_percent": gross_spread_percent,
            "buy_fee_usd": buy_fee_usd,
            "sell_fee_usd": sell_fee_usd,
            "withdrawal_fee_usd": withdrawal_fee_usd,
            "slippage_usd": slippage_usd,
            "latency_penalty_usd": latency_penalty_usd,
            "estimated_fees": buy_fee_usd + sell_fee_usd,
            "net_profit": net_profit,
            "net_profit_percent": net_profit_percent,
            "is_profitable": net_profit > Decimal('0')
        }
