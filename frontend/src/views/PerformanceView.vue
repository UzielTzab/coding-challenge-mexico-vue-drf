<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Rendimiento</h2>
      <p class="text-muted">Gráficos históricos de métricas de P&L.</p>
    </div>
    
    <AppCard class="chart-card">
      <div class="placeholder">
        <p>Los gráficos de Chart.js se implementarán aquí.</p>
      </div>
    </AppCard>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.view-header h2 { margin: 0 0 8px 0; }
.view-header p { margin: 0; }
.chart-card { height: 400px; display: flex; align-items: center; justify-content: center; }
.placeholder { color: var(--color-text-muted); }
</style>
