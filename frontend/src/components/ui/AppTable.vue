<script setup lang="ts">
import AppEmptyState from './AppEmptyState.vue';

interface Props {
  columns: Array<{ key: string; label: string; align?: 'left' | 'center' | 'right' }>;
  data: any[];
  loading?: boolean;
}

defineProps<Props>();
</script>

<template>
  <div class="app-table-container">
    <table v-if="data.length > 0 && !loading" class="app-table">
      <thead>
        <tr>
          <th 
            v-for="col in columns" 
            :key="col.key"
            :style="{ textAlign: col.align || 'left' }"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td 
            v-for="col in columns" 
            :key="col.key"
            :style="{ textAlign: col.align || 'left' }"
          >
            <slot :name="col.key" :item="row">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="loading" class="table-loading">
      <p class="text-muted">Cargando datos...</p>
    </div>
    
    <AppEmptyState v-if="!loading && data.length === 0" message="No hay datos disponibles" />
  </div>
</template>

<style scoped>
.app-table-container {
  width: 100%;
  overflow-x: auto;
}

.app-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm, 14px);
}

.app-table th {
  color: var(--color-text-secondary);
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}

.app-table td {
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  color: var(--color-text-primary);
}

.app-table tbody tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

.table-loading {
  padding: 32px;
  text-align: center;
}
</style>
