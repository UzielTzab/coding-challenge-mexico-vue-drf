<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AppCard from '../components/ui/AppCard.vue';
import WalletCard from '../components/wallets/WalletCard.vue';
import WalletMovementTable from '../components/wallets/WalletMovementTable.vue';
// import { getWallets } from '../services/wallets.service'; // Si tuvieramos este endpoint

const isLoading = ref(false);

const wallets = ref([
  {
    exchange: 'binance',
    totalUsdValue: 15430.50,
    balances: { 'USDT': 10000, 'BTC': 0.15, 'ETH': 2.5 } as Record<string, number>
  },
  {
    exchange: 'kraken',
    totalUsdValue: 12100.20,
    balances: { 'USD': 5000, 'BTC': 0.12, 'ETH': 3.1 } as Record<string, number>
  }
]);

const movements = ref([
  { id: 1, timestamp: new Date().toISOString(), exchange: 'binance', asset: 'USDT', type: 'deposit', amount: 5000, status: 'Completado' },
  { id: 2, timestamp: new Date(Date.now() - 86400000).toISOString(), exchange: 'kraken', asset: 'BTC', type: 'withdraw', amount: 0.05, status: 'Completado' }
]);

onMounted(() => {
  // loadData();
});
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Saldos de Exchange</h2>
      <p class="text-muted">Gestión de portafolio y movimientos de capital.</p>
    </div>
    
    <div class="wallets-grid">
      <WalletCard 
        v-for="w in wallets" 
        :key="w.exchange" 
        :exchange="w.exchange"
        :balances="w.balances"
        :totalUsdValue="w.totalUsdValue"
      />
    </div>

    <div class="movements-section">
      <h3>Historial de Movimientos</h3>
      <AppCard>
        <WalletMovementTable :movements="movements" :isLoading="isLoading" />
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.view-header h2 { margin: 0 0 8px 0; }
.view-header p { margin: 0; }

.wallets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.movements-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: var(--color-text-primary);
}
</style>
