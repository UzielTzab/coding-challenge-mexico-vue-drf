export interface MarketData {
  exchange: string;
  pair: string;
  bid: number;
  ask: number;
  timestamp: string;
}

export interface Opportunity {
  id: string;
  buy_exchange: string;
  sell_exchange: string;
  profit_usd: number;
  profit_percent: number;
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
