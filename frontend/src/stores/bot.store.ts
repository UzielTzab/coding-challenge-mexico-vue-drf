import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useBotStore = defineStore('bot', () => {
  const status = ref<'running' | 'paused' | 'stopped'>('stopped');
  const latency = ref(0);
  
  const setStatus = (newStatus: 'running' | 'paused' | 'stopped') => {
    status.value = newStatus;
  };

  const setLatency = (ms: number) => {
    latency.value = ms;
  };

  return { status, latency, setStatus, setLatency };
});
