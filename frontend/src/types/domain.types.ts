export interface MarketData {
  exchange: string;
  pair: string;
  bid: number;
  ask: number;
  bidVolume?: number;
  askVolume?: number;
  timestamp: string;
}

export interface Opportunity {
  id: string;
  pair?: string;
  symbol?: string;
  buy_exchange: string;
  sell_exchange: string;
  profit_usd: number;
  profit_percent: number;
  spread_percent?: number;
  net_profit?: number;
  status: string;
  timestamp: string;
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
