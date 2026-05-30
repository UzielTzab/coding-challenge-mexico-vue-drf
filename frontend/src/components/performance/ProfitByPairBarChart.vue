<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
import { useFormatters } from '../../composables/useFormatters';

import { computed } from 'vue';

const props = defineProps<{
  data: { pair: string; profit: number }[];
}>();

const { formatUSD } = useFormatters();

const maxProfit = computed(() => Math.max(...(props.data?.map(d => d.profit) || [1])));
</script>

<template>
  <AppCard class="chart-card">
    <div class="chart-header">
      <span class="uppercase-label">Ganancia Neta por Par</span>
    </div>
    <div class="bars-container">
      <div v-for="item in data" :key="item.pair" class="bar-row">
        <div class="bar-label">{{ item.pair }}</div>
        <div class="bar-track">
          <div class="bar-fill" :style="{ width: `${(item.profit / maxProfit) * 100}%` }"></div>
        </div>
        <div class="bar-value text-success">+{{ formatUSD(item.profit) }}</div>
      </div>
    </div>
  </AppCard>
</template>

<style scoped>
.chart-card {
  height: 100%;
}

.chart-header {
  margin-bottom: 24px;
}

.bars-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.bar-label {
  width: 80px;
  font-weight: 500;
  font-size: 13px;
}

.bar-track {
  flex-grow: 1;
  height: 8px;
  background: var(--color-bg-secondary);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.bar-value {
  width: 70px;
  text-align: right;
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
}
</style>
