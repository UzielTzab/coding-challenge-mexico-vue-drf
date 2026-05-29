<script setup lang="ts">
import AppTable from '../ui/AppTable.vue';
import { useFormatters } from '../../composables/useFormatters';

const props = defineProps<{
  operations: any[];
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'row-click', operation: any): void;
}>();

const { formatUSD, formatDate } = useFormatters();

const columns = [
  { key: 'id', label: 'ID Operación' },
  { key: 'pair', label: 'Par' },
  { key: 'side', label: 'Tipo' },
  { key: 'exchange', label: 'Exchange' },
  { key: 'amount', label: 'Cantidad' },
  { key: 'price', label: 'Precio Ejecutado' },
  { key: 'timestamp', label: 'Fecha / Hora' }
];

const handleRowClick = (row: any) => {
  emit('row-click', row);
};
</script>

<template>
  <div class="operation-history">
    <AppTable 
      :columns="columns" 
      :data="operations" 
      :loading="isLoading"
      @row-click="handleRowClick"
    >
      <template #cell-id="{ item }">
        <span class="text-muted">#{{ item.id?.slice(0, 8) }}</span>
      </template>
      <template #cell-pair="{ item }">
        <strong>{{ item.pair }}</strong>
      </template>
      <template #cell-side="{ item }">
        <span :class="item.side === 'buy' ? 'text-success' : 'text-danger'">
          {{ item.side?.toUpperCase() }}
        </span>
      </template>
      <template #cell-price="{ item }">
        {{ formatUSD(item.price) }}
      </template>
      <template #cell-timestamp="{ item }">
        <span class="text-muted">{{ formatDate(item.timestamp) }}</span>
      </template>
    </AppTable>
  </div>
</template>

<style scoped>
.operation-history {
  width: 100%;
}
</style>
