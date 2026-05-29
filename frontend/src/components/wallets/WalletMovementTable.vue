<script setup lang="ts">
import AppTable from '../ui/AppTable.vue';
import { useFormatters } from '../../composables/useFormatters';

const props = defineProps<{
  movements: any[];
  isLoading?: boolean;
}>();

const { formatDate } = useFormatters();

const columns = [
  { key: 'timestamp', label: 'Fecha' },
  { key: 'exchange', label: 'Exchange' },
  { key: 'asset', label: 'Activo' },
  { key: 'type', label: 'Tipo de Movimiento' },
  { key: 'amount', label: 'Cantidad' },
  { key: 'status', label: 'Estado' }
];
</script>

<template>
  <div class="wallet-movements">
    <AppTable 
      :columns="columns" 
      :data="movements" 
      :loading="isLoading"
    >
      <template #cell-timestamp="{ item }">
        <span class="text-muted">{{ formatDate(item.timestamp) }}</span>
      </template>
      <template #cell-exchange="{ item }">
        <span style="text-transform: capitalize;">{{ item.exchange }}</span>
      </template>
      <template #cell-type="{ item }">
        <span :class="item.type === 'deposit' ? 'text-success' : 'text-danger'">
          {{ item.type === 'deposit' ? 'Depósito' : 'Retiro' }}
        </span>
      </template>
      <template #cell-amount="{ item }">
        <span class="numeric">{{ item.type === 'deposit' ? '+' : '-' }}{{ item.amount }} {{ item.asset }}</span>
      </template>
      <template #cell-status="{ item }">
        <span class="text-muted">{{ item.status || 'Completado' }}</span>
      </template>
    </AppTable>
  </div>
</template>

<style scoped>
.wallet-movements {
  width: 100%;
}
</style>
