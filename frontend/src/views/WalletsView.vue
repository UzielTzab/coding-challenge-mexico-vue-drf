<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
import AppTable from '../components/ui/AppTable.vue';
import { useWalletsStore } from '../stores/wallets.store';
import { useFormatters } from '../composables/useFormatters';
import { computed } from 'vue';

const store = useWalletsStore();
const { formatUSD } = useFormatters();

const columns = [
  { key: 'exchange', label: 'Exchange' },
  { key: 'asset', label: 'Activo' },
  { key: 'balance', label: 'Balance Libre', align: 'right' as const },
  { key: 'locked', label: 'En Órdenes', align: 'right' as const },
  { key: 'total', label: 'Total Estimado (USD)', align: 'right' as const }
];

const data = computed(() => {
  return Object.values(store.items).map(w => ({
    ...w,
    total: w.asset === 'USD' ? (w.balance + w.locked) : (w.balance + w.locked) * 60000 // placeholder USD conversion
  }));
});
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Saldos y Wallets</h2>
      <p class="text-muted">Balance detallado en todos los exchanges conectados.</p>
    </div>
    
    <AppCard>
      <AppTable :columns="columns" :data="data">
        <template #balance="{ item }">
          <span class="numeric">{{ item.balance.toFixed(4) }} {{ item.asset }}</span>
        </template>
        <template #locked="{ item }">
          <span class="numeric text-muted">{{ item.locked.toFixed(4) }} {{ item.asset }}</span>
        </template>
        <template #total="{ item }">
          <span class="numeric font-bold">{{ formatUSD(item.total) }}</span>
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
.font-bold { font-weight: 700; }
</style>
