<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
</script>

<template>
  <AppCard class="charts">
    <h3>Rendimiento (P&L)</h3>
    <p class="text-muted">Cargando gráfico...</p>
  </AppCard>
</template>

<style scoped>
.charts { height: 100%; }
h3 { margin: 0 0 12px 0; font-size: 16px; }
</style>
