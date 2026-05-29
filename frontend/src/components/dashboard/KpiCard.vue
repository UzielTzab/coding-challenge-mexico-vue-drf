<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';

interface Props {
  title: string;
  value: string | number;
  variation?: number;
  prefix?: string;
  suffix?: string;
}

defineProps<Props>();
</script>

<template>
  <AppCard class="kpi-card" variant="soft">
    <div class="kpi-label uppercase-label">{{ title }}</div>
    <div class="kpi-value-row">
      <span class="kpi-value numeric">{{ prefix }}{{ value }}{{ suffix }}</span>
      <span v-if="variation" class="kpi-variation" :class="variation > 0 ? 'text-success' : 'text-danger'">
        {{ variation > 0 ? '▲' : '▼' }} {{ Math.abs(variation) }}%
      </span>
    </div>
  </AppCard>
</template>

<style scoped>
.kpi-card {
  background: var(--color-bg-base);
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px 24px;
}
.kpi-label { margin-bottom: 4px; }
.kpi-value-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.kpi-value {
  font-size: 28px;
  font-weight: 500;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}
.kpi-variation {
  font-size: 12px;
  font-weight: 600;
}
</style>
