<script setup lang="ts">
import AppCard from '../components/ui/AppCard.vue';
import { useLogsStore } from '../stores/logs.store';
import { computed } from 'vue';

const store = useLogsStore();
const logs = computed(() => store.items);
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Registros del Sistema</h2>
      <p class="text-muted">Consola histórica de todos los eventos del bot.</p>
    </div>
    
    <AppCard variant="terminal" class="log-card">
      <div class="log-body">
        <div v-for="log in logs" :key="log.id" class="log-line">
          <span class="log-time">{{ new Date(log.timestamp).toLocaleString() }}</span>
          <span :class="['log-level', `log-level--${log.level.toLowerCase()}`]">[ {{ log.level }} ]</span>
          <span class="log-msg">{{ log.message }}</span>
        </div>
        <div v-if="logs.length === 0" class="text-muted text-center mt-4">No hay registros disponibles.</div>
      </div>
    </AppCard>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: calc(100vh - 120px);
}
.view-header h2 { margin: 0 0 8px 0; }
.view-header p { margin: 0; }
.log-card { flex-grow: 1; display: flex; flex-direction: column; }
.log-body { flex-grow: 1; overflow-y: auto; font-size: 14px; }
.log-line { margin-bottom: 6px; display: flex; gap: 12px; }
.log-time { color: var(--color-text-muted); }
.log-level--info { color: var(--color-primary-light); }
.log-level--success { color: var(--color-success); }
.log-level--warning { color: var(--color-warning); }
.log-level--error { color: var(--color-danger); }
.log-msg { color: var(--color-text-primary); }
</style>
