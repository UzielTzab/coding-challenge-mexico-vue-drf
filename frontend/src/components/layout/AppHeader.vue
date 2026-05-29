<script setup lang="ts">
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const pageTitle = computed(() => route.meta.title || 'ArbiBTC');
</script>

<template>
  <header class="app-header">
    <div class="header-title">
      <h2>{{ pageTitle }}</h2>
    </div>
    
    <div class="header-status">
      <div class="status-item">
        <span class="status-dot success"></span>
        <span class="text-muted">Backend</span>
      </div>
      <div class="status-item">
        <span class="status-dot success"></span>
        <span class="text-muted">WS</span>
      </div>
      <div class="status-item">
        <span class="status-dot success"></span>
        <span class="text-muted">Motor Bot</span>
      </div>
      <div class="status-item">
        <span class="text-muted">Latencia: <span class="numeric text-success">28ms</span></span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: var(--header-height, 72px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--content-padding, 24px);
  background: var(--color-bg-dashboard);
  border-bottom: 1px solid var(--color-border);
}

.header-title h2 {
  margin: 0;
  font-size: var(--text-lg, 18px);
  font-weight: 600;
}

.header-status {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: var(--text-xs, 12px);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.success {
  background: var(--color-success);
  box-shadow: 0 0 8px rgba(3, 185, 135, 0.4);
}
</style>
