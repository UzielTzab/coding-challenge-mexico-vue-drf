<script setup lang="ts">
import { computed } from 'vue';
import AppCard from '../ui/AppCard.vue';
import { useLogsStore } from '../../stores/logs.store';

const store = useLogsStore();
const logs = computed(() => store.items.slice(0, 50));
</script>

<template>
  <AppCard variant="terminal" class="log-panel">
    <div class="log-header">Terminal del Sistema</div>
    <div class="log-body">
      <div v-for="log in logs" :key="log.id" class="log-line">
        <span class="log-time">{{ new Date(log.timestamp).toLocaleTimeString() }}</span>
        <span :class="['log-level', `log-level--${log.level.toLowerCase()}`]">[ {{ log.level }} ]</span>
        <span class="log-msg">{{ log.message }}</span>
      </div>
      <div v-if="logs.length === 0" class="text-muted">Esperando logs del sistema...</div>
    </div>
  </AppCard>
</template>

<style scoped>
.log-panel {
  display: flex;
  flex-direction: column;
  height: 300px;
}
.log-header {
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 8px;
  margin-bottom: 8px;
  font-size: 12px;
  color: var(--color-text-secondary);
}
.log-body {
  flex-grow: 1;
  overflow-y: auto;
  font-size: 13px;
  display: flex;
  flex-direction: column-reverse;
}
.log-line {
  margin-bottom: 4px;
  display: flex;
  gap: 8px;
}
.log-time { color: var(--color-text-muted); }
.log-level--info { color: var(--color-primary-light); }
.log-level--success { color: var(--color-success); }
.log-level--warning { color: var(--color-warning); }
.log-level--error { color: var(--color-danger); }
.log-msg { color: var(--color-text-primary); }
</style>
