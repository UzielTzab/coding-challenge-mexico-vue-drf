<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
import PnlLineChart from '../performance/PnlLineChart.vue';
</script>

<template>
  <AppCard class="charts">
    <h3>Historial de P&L</h3>
    <PnlLineChart :data="[10, 25, 45, 120, 310, 450]" />
  </AppCard>
</template>

<style scoped>
.charts { height: 100%; }
h3 { margin: 0 0 12px 0; font-size: 16px; }
</style>
