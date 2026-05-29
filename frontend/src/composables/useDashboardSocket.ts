import { watch } from 'vue';
import { useWebSocket } from './useWebSocket';
import { useMarketStore } from '../stores/market.store';
import { useOpportunitiesStore } from '../stores/opportunities.store';

export const useDashboardSocket = () => {
  const wsUrl = (import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000') + '/ws/dashboard/';
  const { ws, isConnected, connect } = useWebSocket(wsUrl);
  
  const marketStore = useMarketStore();
  const oppStore = useOpportunitiesStore();

  watch(ws, (socket) => {
    if (socket) {
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'market_update') {
          marketStore.upsertSnapshot(data.payload);
        } else if (data.type === 'opportunity_detected') {
          oppStore.prepend(data.payload);
        }
      };
    }
  });

  return { isConnected, connect };
};
