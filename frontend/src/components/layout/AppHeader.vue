<script setup lang="ts">
import { useRoute } from 'vue-router';
import { computed, ref, onMounted } from 'vue';
import { getSettings, updateSettings } from '../../services/settings.service';
import { useBotStore } from '../../stores/bot.store';

const route = useRoute();
const botStore = useBotStore();
const settingId = ref<string | null>(null);
const backendStatus = ref(true);
const wsStatus = ref(true); // Se asume verdadero al inicio si no hay fallos en consola

const pageTitle = computed(() => {
  const map: Record<string, string> = {
    '/': 'Overview',
    '/markets': 'Mercados',
    '/opportunities': 'Oportunidades',
    '/operations': 'Operaciones',
    '/wallets': 'Saldos de Exchange',
    '/performance': 'Rendimiento',
    '/logs': 'Consola del Sistema',
    '/settings': 'Configuración'
  };
  return map[route.path] || 'Dashboard';
});

const loadSettings = async () => {
  try {
    const data = await getSettings();
    const results = data.results || data;
    if (results && results.length > 0) {
      settingId.value = results[0].id;
      botStore.setStatus(results[0].is_running ? 'running' : 'stopped');
      backendStatus.value = true;
    }
  } catch (error) {
    console.error('Error fetching settings for bot toggle', error);
    backendStatus.value = false;
    wsStatus.value = false;
  }
};

const toggleBot = async (state: boolean) => {
  if (!settingId.value) return;
  try {
    await updateSettings(settingId.value, { is_running: state });
    botStore.setStatus(state ? 'running' : 'stopped');
    backendStatus.value = true;
  } catch (error) {
    console.error('Error toggling bot', error);
    backendStatus.value = false;
  }
};

onMounted(() => {
  loadSettings();
});
</script>

<template>
  <header class="header">
    <div class="header-title">
      <h1>{{ pageTitle }}</h1>
    </div>
    
    <div class="header-actions">
      <div class="status-indicators">
        <div class="status">
          <span class="status-dot" :class="backendStatus ? 'status-dot--success' : 'status-dot--danger'"></span>
          <span class="text-sm text-muted">Backend {{ backendStatus ? 'OK' : 'Error' }}</span>
        </div>
        <div class="status">
          <span class="status-dot" :class="wsStatus ? 'status-dot--success' : 'status-dot--danger'"></span>
          <span class="text-sm text-muted">WS {{ wsStatus ? 'OK' : 'Error' }}</span>
        </div>
      </div>
      
      <div class="action-buttons">
        <button v-if="botStore.status !== 'running'" class="btn-dark" @click="toggleBot(true)">Iniciar Bot</button>
        <button v-else class="btn-dark" style="background-color: var(--color-danger)" @click="toggleBot(false)">Pausar Bot</button>
      </div>

      <div class="profile-section">
        <span class="material-symbols-outlined notification-icon">notifications</span>
        <div class="avatar"></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  height: 80px;
  min-height: 80px;
  flex-shrink: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.header-title h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 32px;
}

.status-indicators {
  display: flex;
  gap: 24px;
}

.status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot--success { background: var(--color-success); }
.status-dot--danger { background: var(--color-danger); }

.action-buttons {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-dark {
  background: #252836;
  color: var(--color-text-primary);
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
  transition: background 150ms;
}
.btn-dark:hover { background: #303446; }

.btn-text {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
}
.btn-text:hover { color: var(--color-text-primary); }

.profile-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-left: 24px;
  border-left: 1px solid var(--color-border);
}

.notification-icon {
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 20px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Felix') no-repeat center/cover;
  background-color: var(--color-bg-card-soft);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.text-sm { font-size: 13px; }
</style>
