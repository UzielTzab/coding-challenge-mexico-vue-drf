<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
import AppTable from '../components/ui/AppTable.vue';
import { useMarketStore } from '../stores/market.store';
import { useFormatters } from '../composables/useFormatters';
import { computed } from 'vue';

const store = useMarketStore();
const { formatUSD } = useFormatters();

const columns = [
  { key: 'exchange', label: 'Exchange' },
  { key: 'pair', label: 'Par' },
  { key: 'bid', label: 'Best Bid', align: 'right' as const },
  { key: 'ask', label: 'Best Ask', align: 'right' as const },
  { key: 'timestamp', label: 'Última Actualización', align: 'right' as const }
];

const data = computed(() => Object.values(store.snapshots));
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Mercados</h2>
      <p class="text-muted">Estado actual de los libros de órdenes en los exchanges conectados.</p>
    </div>
    
    <AppCard>
      <AppTable :columns="columns" :data="data">
        <template #bid="{ item }">
          <span class="numeric text-success">{{ formatUSD(item.bid) }}</span>
        </template>
        <template #ask="{ item }">
          <span class="numeric text-danger">{{ formatUSD(item.ask) }}</span>
        </template>
        <template #timestamp="{ item }">
          <span class="text-muted">{{ new Date(item.timestamp).toLocaleTimeString() }}</span>
        </template>
      </AppTable>
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
</style>
