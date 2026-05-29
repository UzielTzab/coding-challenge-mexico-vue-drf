import { watch } from 'vue';
import { useWebSocket } from './useWebSocket';
import { useMarketStore } from '../stores/market.store';
import { useLogsStore } from '../stores/logs.store';

export const useDashboardSocket = () => {
  const wsUrl = (import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000') + '/ws/dashboard/';
  const { ws, isConnected, connect } = useWebSocket(wsUrl);
  
  const marketStore = useMarketStore();
  const logsStore = useLogsStore();
  
  // Actually, I'll just map the events according to what is present for now.
  watch(ws, (socket) => {
    if (socket) {
      socket.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'market_update':
            marketStore.upsertSnapshot({
              exchange: data.exchange,
              pair: data.symbol,
              bid: parseFloat(data.best_bid),
              ask: parseFloat(data.best_ask),
              timestamp: new Date().toISOString()
            });
            break;
          case 'system_log_created':
            logsStore.prepend({
              id: Math.random().toString(36).substring(2, 9),
              level: data.level,
              message: data.message,
              timestamp: data.created_at
            });
            break;
          case 'opportunity_detected':
            // oppStore.prepend(data);
            break;
          case 'trade_simulated':
            // tradesStore.prepend(data);
            break;
          case 'wallet_updated':
            // walletsStore.update(data);
            break;
          case 'bot_status_changed':
            // log/performance store update
            break;
        }
      };
    }
  });

  return { isConnected, connect };
};
