<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
import AppBadge from '../ui/AppBadge.vue';
import type { MarketData } from '../../types/domain.types';
import { useFormatters } from '../../composables/useFormatters';

const { formatUSD } = useFormatters();

interface Props {
  exchangeName: string;
  marketData?: MarketData;
  connected?: boolean;
}

defineProps<Props>();
</script>

<template>
  <AppCard>
    <div class="exchange-header">
      <h3>{{ exchangeName }}</h3>
      <AppBadge :variant="connected ? 'success' : 'danger'">
        {{ connected ? 'Conectado' : 'Desconectado' }}
      </AppBadge>
    </div>
    
    <div class="exchange-stats" v-if="marketData">
      <div class="stat">
        <span class="label">Best Bid</span>
        <span class="value text-success">{{ formatUSD(marketData.bid) }}</span>
      </div>
      <div class="stat">
        <span class="label">Best Ask</span>
        <span class="value text-danger">{{ formatUSD(marketData.ask) }}</span>
      </div>
    </div>
    <div v-else class="text-muted empty-state">
      Esperando datos...
    </div>
  </AppCard>
</template>

<style scoped>
.exchange-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.exchange-header h3 { margin: 0; font-size: 16px; }
.exchange-stats { display: flex; flex-direction: column; gap: 8px; }
.stat { display: flex; justify-content: space-between; font-size: 14px; }
.empty-state { text-align: center; padding: 20px 0; font-size: 14px; }
</style>
