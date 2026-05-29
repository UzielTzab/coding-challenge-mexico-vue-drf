import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { MarketData } from '../types/domain.types';

export const useMarketStore = defineStore('market', () => {
  const snapshots = ref<Record<string, MarketData>>({});
  
  const upsertSnapshot = (data: MarketData) => {
    snapshots.value[`${data.exchange}-${data.pair}`] = data;
  };

  return { snapshots, upsertSnapshot };
});
