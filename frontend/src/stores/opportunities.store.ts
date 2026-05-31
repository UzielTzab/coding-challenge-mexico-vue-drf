import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Opportunity } from '../types/domain.types';

export const useOpportunitiesStore = defineStore('opportunities', () => {
  const items = ref<Opportunity[]>([]);
  const totalPnl = ref(0);
  const pnlHistory = ref<{date: string, value: number}[]>([]);
  
  const summary = ref({
    global_win_rate: 0,
    trades_count: 0,
    discarded_opportunities: 0,
    opportunities_count: 0,
    average_cost: 0
  });

  const prepend = (opp: Opportunity) => {
    items.value.unshift(opp);
    
    // Update real-time counts
    summary.value.opportunities_count++;
    if (opp.status === 'executed' || opp.status === 'profitable') {
      summary.value.trades_count++;
    } else if (opp.status === 'discarded') {
      summary.value.discarded_opportunities++;
    }

    if (opp.status === 'profitable' && opp.net_profit) {
      const profitValue = typeof opp.net_profit === 'string' ? parseFloat(opp.net_profit) : opp.net_profit;
      totalPnl.value += profitValue;
      
      // Update chart history
      const now = new Date();
      pnlHistory.value.push({
        date: now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
        value: totalPnl.value
      });
      // Keep only last 20 points for smooth scrolling chart
      if (pnlHistory.value.length > 20) {
        pnlHistory.value.shift();
      }
    }
  };

  const setInitialPnl = (initialPnl: number) => {
    totalPnl.value = initialPnl;
    if (pnlHistory.value.length === 0) {
      pnlHistory.value.push({
        date: new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }),
        value: initialPnl
      });
    }
  };

  const setSummary = (s: any) => {
    summary.value = { ...summary.value, ...s };
  };

  return { items, prepend, totalPnl, pnlHistory, setInitialPnl, summary, setSummary };
});
