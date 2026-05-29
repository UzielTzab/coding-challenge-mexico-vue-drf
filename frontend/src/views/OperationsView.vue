<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
import AppTable from '../components/ui/AppTable.vue';
import AppBadge from '../components/ui/AppBadge.vue';
import { useTradesStore } from '../stores/trades.store';
import { useFormatters } from '../composables/useFormatters';
import { computed } from 'vue';

const store = useTradesStore();
const { formatUSD } = useFormatters();

const columns = [
  { key: 'id', label: 'Trade ID' },
  { key: 'opportunity_id', label: 'Opp ID' },
  { key: 'net_profit', label: 'Profit Neto', align: 'right' as const },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'executed_at', label: 'Fecha de Ejecución', align: 'right' as const }
];

const data = computed(() => store.items);

const getBadgeVariant = (status: string) => {
  if (status === 'completed') return 'success';
  if (status === 'failed') return 'danger';
  if (status === 'pending') return 'warning';
  return 'neutral';
};
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Operaciones Ejecutadas</h2>
      <p class="text-muted">Registro de todas las operaciones enviadas a los exchanges.</p>
    </div>
    
    <AppCard>
      <AppTable :columns="columns" :data="data">
        <template #id="{ item }">
          <span class="text-muted text-xs">{{ item.id.substring(0, 8) }}</span>
        </template>
        <template #opportunity_id="{ item }">
          <span class="text-muted text-xs">{{ item.opportunity_id.substring(0, 8) }}</span>
        </template>
        <template #net_profit="{ item }">
          <span :class="['numeric', item.net_profit > 0 ? 'text-success' : 'text-danger']">
            {{ formatUSD(item.net_profit) }}
          </span>
        </template>
        <template #status="{ item }">
          <AppBadge :variant="getBadgeVariant(item.status)">{{ item.status }}</AppBadge>
        </template>
        <template #executed_at="{ item }">
          <span class="text-muted">{{ new Date(item.executed_at).toLocaleString() }}</span>
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
