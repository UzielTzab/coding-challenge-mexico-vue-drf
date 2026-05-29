<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
// Asumimos el uso de Chart.js o similar, pero por ahora mostramos un placeholder estilizado
// ya que no hay una librería de charts instalada explícitamente en el setup base.

const props = defineProps<{
  data: any[];
  title?: string;
}>();
</script>

<template>
  <AppCard class="chart-card">
    <div class="chart-header">
      <span class="uppercase-label">{{ title || 'Evolución del P&L' }}</span>
    </div>
    <div class="chart-container">
      <div v-if="!data || data.length === 0" class="empty-chart text-muted">
        No hay suficientes datos para graficar
      </div>
      <div v-else class="mock-chart">
        <!-- Mock visual de un chart de línea -->
        <svg viewBox="0 0 100 30" class="line-svg" preserveAspectRatio="none">
          <path d="M0,25 L10,22 L20,24 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0" 
                fill="none" stroke="var(--color-primary)" stroke-width="2" />
          <path d="M0,25 L10,22 L20,24 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0 L100,30 L0,30 Z" 
                fill="url(#gradient)" stroke="none" />
          <defs>
            <linearGradient id="gradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--color-primary)" stop-opacity="0.3" />
              <stop offset="100%" stop-color="var(--color-primary)" stop-opacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>
  </AppCard>
</template>

<style scoped>
.chart-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-header {
  margin-bottom: 16px;
}

.chart-container {
  flex-grow: 1;
  min-height: 200px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.mock-chart {
  width: 100%;
  height: 100%;
  padding-top: 20px;
}

.line-svg {
  width: 100%;
  height: 100%;
}
</style>
