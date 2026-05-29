<script setup lang="ts">
import { computed } from 'vue';
import AppCard from '../ui/AppCard.vue';
import AppTable from '../ui/AppTable.vue';
import AppBadge from '../ui/AppBadge.vue';
import AppButton from '../ui/AppButton.vue';
import { useOpportunitiesStore } from '../../stores/opportunities.store';
import { useFormatters } from '../../composables/useFormatters';


const store = useOpportunitiesStore();
const { formatUSD, formatPercent } = useFormatters();

const columns = [
  { key: 'buy_exchange', label: 'Comprar en' },
  { key: 'sell_exchange', label: 'Vender en' },
  { key: 'profit_usd', label: 'Profit USD', align: 'right' as const },
  { key: 'profit_percent', label: 'Profit %', align: 'right' as const },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'actions', label: 'Acción', align: 'center' as const }
];

const data = computed(() => store.items.slice(0, 10)); // Mostrar top 10

const getBadgeVariant = (status: string) => {
  if (status === 'rentable') return 'success';
  if (status === 'descartada') return 'danger';
  if (status === 'ejecutada') return 'info';
  return 'neutral';
};
</script>

<template>
  <AppCard class="opp-card" variant="soft">
    <div class="opp-header">
      <h3>Oportunidades en Tiempo Real</h3>
    </div>
    <AppTable :columns="columns" :data="data">
      <template #profit_usd="{ item }">
        <span class="numeric text-success">+{{ formatUSD(item.profit_usd) }}</span>
      </template>
      <template #profit_percent="{ item }">
        <span class="numeric text-success">{{ formatPercent(item.profit_percent) }}</span>
      </template>
      <template #status="{ item }">
        <AppBadge :variant="getBadgeVariant(item.status)">{{ item.status }}</AppBadge>
      </template>
      <template #actions="{ item }">
        <AppButton variant="secondary" @click="$emit('view', item)">Ver</AppButton>
      </template>
    </AppTable>
  </AppCard>
</template>

<style scoped>
.opp-card { display: flex; flex-direction: column; height: 100%; }
.opp-header { margin-bottom: 16px; }
.opp-header h3 { margin: 0; font-size: 16px; }
</style>
