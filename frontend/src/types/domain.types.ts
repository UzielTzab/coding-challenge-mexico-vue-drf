export interface MarketData {
  exchange: string;
  pair: string;
  bid: number;
  ask: number;
  bidVolume?: number;
  askVolume?: number;
  timestamp: string;
  latency_ms?: number;
}

export interface Opportunity {
  id: string;
  pair?: string;
  symbol?: string;
  buy_exchange: string;
  sell_exchange: string;
  buy_exchange_name?: string;
  sell_exchange_name?: string;
  profit_usd: number;
  profit_percent: number;
  spread_percent?: number;
  gross_spread_percent?: number;
  net_profit?: number;
  status: string;
  timestamp: string;
  detected_at?: string;
}

export interface Trade {
  id: string;
  opportunity_id: string;
  status: string;
  net_profit: number;
  executed_at: string;
}

export interface Wallet {
  exchange: string;
  asset: string;
  balance: number;
  locked: number;
}
