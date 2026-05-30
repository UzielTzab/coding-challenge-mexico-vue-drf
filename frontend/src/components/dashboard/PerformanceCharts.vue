<script setup lang="ts">
import PnlLineChart from '../performance/PnlLineChart.vue';
</script>

<template>
  <div class="charts-wrapper">
    <PnlLineChart :data="[10, 25, 45, 120, 310, 450]" />
  </div>
</template>

<style scoped>
.charts-wrapper { height: 100%; min-height: 300px; display: flex; flex-direction: column; }
.charts-wrapper > * { flex-grow: 1; }
</style>
