import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { MarketData } from '../types/domain.types';

export const useMarketStore = defineStore('market', () => {
  const snapshots = ref<Record<string, MarketData>>({});
  
  const upsertSnapshot = (data: MarketData) => {
    const key = `${data.exchange}-${data.pair}`;
    if (snapshots.value[key]) {
      // Muta las propiedades en el proxy reactivo existente
      snapshots.value[key].bid = data.bid;
      snapshots.value[key].ask = data.ask;
      if (data.bidVolume) snapshots.value[key].bidVolume = data.bidVolume;
      if (data.askVolume) snapshots.value[key].askVolume = data.askVolume;
      snapshots.value[key].timestamp = data.timestamp;
    } else {
      // Crea el proxy por primera vez
      snapshots.value[key] = data;
    }
  };

  return { snapshots, upsertSnapshot };
});
