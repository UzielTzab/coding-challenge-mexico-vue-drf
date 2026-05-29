<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
import AppTable from '../components/ui/AppTable.vue';
import AppBadge from '../components/ui/AppBadge.vue';
import { useOpportunitiesStore } from '../stores/opportunities.store';
import { useFormatters } from '../composables/useFormatters';
import { computed } from 'vue';

const store = useOpportunitiesStore();
const { formatUSD, formatPercent } = useFormatters();

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'buy_exchange', label: 'Comprar' },
  { key: 'sell_exchange', label: 'Vender' },
  { key: 'profit_usd', label: 'Ganancia USD', align: 'right' as const },
  { key: 'profit_percent', label: 'Ganancia %', align: 'right' as const },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'timestamp', label: 'Fecha' }
];

const data = computed(() => store.items);

const getBadgeVariant = (status: string) => {
  if (status === 'rentable') return 'success';
  if (status === 'descartada') return 'danger';
  if (status === 'ejecutada') return 'info';
  return 'neutral';
};
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Oportunidades de Arbitraje</h2>
      <p class="text-muted">Historial completo de las oportunidades detectadas por el sistema.</p>
    </div>
    
    <AppCard>
      <AppTable :columns="columns" :data="data">
        <template #id="{ item }">
          <span class="text-muted text-xs">{{ item.id.substring(0, 8) }}</span>
        </template>
        <template #profit_usd="{ item }">
          <span class="numeric text-success">+{{ formatUSD(item.profit_usd) }}</span>
        </template>
        <template #profit_percent="{ item }">
          <span class="numeric text-success">{{ formatPercent(item.profit_percent) }}</span>
        </template>
        <template #status="{ item }">
          <AppBadge :variant="getBadgeVariant(item.status)">{{ item.status }}</AppBadge>
        </template>
        <template #timestamp="{ item }">
          <span class="text-muted">{{ new Date(item.timestamp).toLocaleString() }}</span>
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
.text-xs { font-size: 12px; }
</style>
