<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
import { useWalletsStore } from '../../stores/wallets.store';

const store = useWalletsStore();
</script>

<template>
  <AppCard class="wallet-summary">
    <h3>Saldos de Wallets</h3>
    <p class="text-muted" v-if="Object.keys(store.items).length === 0">No hay saldos registrados aún.</p>
    <div v-else class="wallet-list">
      <!-- Se pintarán los saldos aquí -->
    </div>
  </AppCard>
</template>

<style scoped>
.wallet-summary { height: 100%; }
h3 { margin: 0 0 12px 0; font-size: 16px; }
</style>
