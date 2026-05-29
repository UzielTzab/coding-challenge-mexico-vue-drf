import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Opportunity } from '../types/domain.types';

export const useOpportunitiesStore = defineStore('opportunities', () => {
  const items = ref<Opportunity[]>([]);
  
  const prepend = (opp: Opportunity) => {
    items.value.unshift(opp);
  };

  return { items, prepend };
});
