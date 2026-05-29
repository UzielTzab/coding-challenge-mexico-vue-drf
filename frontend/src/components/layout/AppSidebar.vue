<script setup lang="ts">
</script>

<template>
  <aside class="app-sidebar">
    <div class="sidebar-header">
      <h1 class="logo">ArbiBTC</h1>
      <p class="subtitle text-muted">Bitcoin Arbitrage Bot</p>
    </div>
    
    <nav class="sidebar-nav">
      <router-link to="/" class="sidebar-link" active-class="sidebar-link--active">Dashboard</router-link>
      <router-link to="/markets" class="sidebar-link" active-class="sidebar-link--active">Mercados</router-link>
      <router-link to="/opportunities" class="sidebar-link" active-class="sidebar-link--active">Oportunidades</router-link>
      <router-link to="/operations" class="sidebar-link" active-class="sidebar-link--active">Operaciones</router-link>
      <router-link to="/wallets" class="sidebar-link" active-class="sidebar-link--active">Wallets</router-link>
      <router-link to="/performance" class="sidebar-link" active-class="sidebar-link--active">Rendimiento</router-link>
      <router-link to="/logs" class="sidebar-link" active-class="sidebar-link--active">Logs</router-link>
      <router-link to="/settings" class="sidebar-link" active-class="sidebar-link--active">Configuración</router-link>
    </nav>
    
    <div class="sidebar-footer">
      <div class="bot-info">
        <p>Modo: <span class="text-success">Simulación</span></p>
        <p class="text-muted">Versión: ArbiBTC v1.0.0</p>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  background: var(--color-bg-sidebar);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-header {
  padding: 24px;
}

.logo {
  font-size: var(--text-xl, 24px);
  font-weight: 800;
  margin: 0 0 4px 0;
}

.subtitle {
  font-size: var(--text-xs, 12px);
  margin: 0;
}

.sidebar-nav {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 16px;
  overflow-y: auto;
}

.sidebar-link {
  height: 44px;
  display: flex;
  align-items: center;
  padding: 0 14px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-secondary);
  font-weight: 500;
  transition: 160ms ease;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary);
}

.sidebar-link--active {
  background: var(--gradient-primary);
  color: #FFFFFF;
  box-shadow: 0 8px 20px rgba(68, 81, 187, 0.35);
}

.sidebar-footer {
  padding: 24px;
  border-top: 1px solid var(--color-border);
}

.bot-info p {
  font-size: var(--text-xs, 12px);
  margin: 0 0 4px 0;
}
</style>
