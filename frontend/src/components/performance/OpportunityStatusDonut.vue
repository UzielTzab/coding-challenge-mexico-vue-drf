<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';

import { computed } from 'vue';

const props = defineProps<{
  stats: {
    executed: number;
    failed: number;
    discarded: number;
  };
}>();

const total = computed(() => props.stats.executed + props.stats.failed + props.stats.discarded);
const getPercent = (val: number) => total.value > 0 ? Math.round((val / total.value) * 100) : 0;
</script>

<template>
  <AppCard class="chart-card">
    <div class="chart-header">
      <span class="uppercase-label">Tasa de Éxito</span>
    </div>
    <div class="donut-container">
      <div class="donut-circle">
        <div class="donut-center">
          <span class="win-rate">{{ getPercent(stats.executed) }}%</span>
          <span class="text-muted text-sm">Win Rate</span>
        </div>
      </div>
      <div class="legend">
        <div class="legend-item">
          <span class="dot success"></span>
          <span>Ejecutadas ({{ stats.executed }})</span>
        </div>
        <div class="legend-item">
          <span class="dot danger"></span>
          <span>Fallidas ({{ stats.failed }})</span>
        </div>
        <div class="legend-item">
          <span class="dot warning"></span>
          <span>Descartadas ({{ stats.discarded }})</span>
        </div>
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

.donut-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 24px;
}

.donut-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: conic-gradient(
    var(--color-success) 0% 75%, 
    var(--color-danger) 75% 85%, 
    var(--color-warning) 85% 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut-center {
  width: 110px;
  height: 110px;
  background: var(--color-bg-card);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.win-rate {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.success { background: var(--color-success); }
.dot.danger { background: var(--color-danger); }
.dot.warning { background: var(--color-warning); }

.text-sm { font-size: 12px; }
</style>
