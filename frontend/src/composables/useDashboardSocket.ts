import { watch } from 'vue';
import { useWebSocket } from './useWebSocket';

export const useDashboardSocket = () => {
  const wsUrl = (import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000') + '/ws/dashboard/';
  const { ws, isConnected, connect } = useWebSocket(wsUrl);
  
  // Actually, I'll just map the events according to what is present for now.
  watch(ws, (socket) => {
    if (socket) {
      socket.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
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
