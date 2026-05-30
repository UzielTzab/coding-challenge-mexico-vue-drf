<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useDashboardSocket } from '../composables/useDashboardSocket';
import { getDashboardSummary, getExchanges } from '../services/dashboard.service';
import { useMarketStore } from '../stores/market.store';
import KpiCard from '../components/dashboard/KpiCard.vue';
import ExchangeCard from '../components/dashboard/ExchangeCard.vue';
import OpportunityTable from '../components/dashboard/OpportunityTable.vue';
import ExecutionPanel from '../components/dashboard/ExecutionPanel.vue';
import WalletSummary from '../components/dashboard/WalletSummary.vue';
import PerformanceCharts from '../components/dashboard/PerformanceCharts.vue';
import SystemLogPanel from '../components/dashboard/SystemLogPanel.vue';
import AppSkeleton from '../components/ui/AppSkeleton.vue';

const { connect } = useDashboardSocket();
const marketStore = useMarketStore();
const isLoading = ref(true);
const summary = ref({
  global_pnl: 0,
  global_win_rate: 0,
  trades_count: 0,
  opportunities_count: 0,
  average_cost: 0
});

onMounted(async () => {
  connect();
  try {
    const data = await getDashboardSummary();
    let result = data.results ? data.results : data;
    if (Array.isArray(result) && result.length > 0) result = result[0];
    
    if (result) {
      summary.value = {
        global_pnl: parseFloat(result.total_pnl_usd) || 0,
        global_win_rate: parseFloat(result.win_rate_percent) || 0,
        trades_count: result.total_trades || 0,
        opportunities_count: (result.total_trades || 0) + (result.discarded_opportunities || 0),
        average_cost: parseFloat(result.total_fees_usd) || 0
      };
    }
  } catch (error) {
    console.error('Error loading dashboard summary', error);
  }

  try {
    const exData = await getExchanges();
    const exchanges = exData.results || exData;
    if (Array.isArray(exchanges)) {
      exchanges.forEach((ex: any) => {
        marketStore.upsertSnapshot({
          exchange: ex.name ? ex.name.toLowerCase() : ex.exchange,
          pair: ex.pair || 'BTC/USDT',
          bid: ex.last_bid || ex.bid || 0,
          ask: ex.last_ask || ex.ask || 0,
          timestamp: new Date().toISOString()
        });
      });
    }
  } catch (error) {
    console.error('Error loading exchanges:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="dashboard-grid">
    <template v-if="isLoading">
      <div v-for="i in 6" :key="`kpi-${i}`" class="col-span-2">
        <AppSkeleton height="100px" borderRadius="12px" />
      </div>
      <div v-for="i in 3" :key="`ex-${i}`" class="col-span-4">
        <AppSkeleton height="220px" borderRadius="12px" />
      </div>
      <div class="col-span-7"><AppSkeleton height="350px" borderRadius="12px" /></div>
      <div class="col-span-5"><AppSkeleton height="350px" borderRadius="12px" /></div>
      <div class="col-span-5"><AppSkeleton height="300px" borderRadius="12px" /></div>
      <div class="col-span-7"><AppSkeleton height="300px" borderRadius="12px" /></div>
      <div class="col-span-12"><AppSkeleton height="250px" borderRadius="12px" /></div>
    </template>
    
    <template v-else>
      <!-- Fila 1: KPIs (6 cards x 2 columnas = 12 cols) -->
      <KpiCard class="col-span-2" title="P&L Total" :value="summary.global_pnl" prefix="$" />
      <KpiCard class="col-span-2" title="Win Rate" :value="summary.global_win_rate" suffix="%" />
      <KpiCard class="col-span-2" title="Ops Ejecutadas" :value="summary.trades_count" />
      <KpiCard class="col-span-2" title="Oportunidades" :value="summary.opportunities_count" />
      <KpiCard class="col-span-2" title="Costo Promedio" :value="summary.average_cost" prefix="$" />
      <KpiCard class="col-span-2" title="Ganancia Neta" :value="summary.global_pnl" prefix="$" />

      <!-- Fila 2: Exchanges (3 cards x 4 columnas = 12 cols) -->
      <ExchangeCard 
        class="col-span-4" 
        exchangeName="Binance" 
        :connected="Object.keys(marketStore.snapshots).some(k => k.includes('binance'))" 
        :marketData="Object.values(marketStore.snapshots).find(m => m.exchange === 'binance')" 
      />
      <ExchangeCard 
        class="col-span-4" 
        exchangeName="Kraken" 
        :connected="Object.keys(marketStore.snapshots).some(k => k.includes('kraken'))" 
        :marketData="Object.values(marketStore.snapshots).find(m => m.exchange === 'kraken')" 
      />
      <ExchangeCard 
        class="col-span-4" 
        exchangeName="Bitfinex" 
        :connected="Object.keys(marketStore.snapshots).some(k => k.includes('bitfinex'))" 
        :marketData="Object.values(marketStore.snapshots).find(m => m.exchange === 'bitfinex')" 
      />

      <!-- Fila 3: Oportunidades y Ejecución -->
      <OpportunityTable class="col-span-7" />
      <ExecutionPanel class="col-span-5" />

      <!-- Fila 4: Wallets y Charts -->
      <WalletSummary class="col-span-5" />
      <PerformanceCharts class="col-span-7" />

      <!-- Fila 5: Terminal -->
      <SystemLogPanel class="col-span-12" />
    </template>
  </div>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
  padding-bottom: 24px;
}

.col-span-2 { grid-column: span 2; }
.col-span-4 { grid-column: span 4; }
.col-span-5 { grid-column: span 5; }
.col-span-7 { grid-column: span 7; }
.col-span-12 { grid-column: span 12; }

@media (max-width: 1200px) {
  .dashboard-grid { grid-template-columns: repeat(6, 1fr); }
  .col-span-2 { grid-column: span 2; }
  .col-span-4 { grid-column: span 6; }
  .col-span-5 { grid-column: span 6; }
  .col-span-7 { grid-column: span 6; }
}

@media (max-width: 768px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .col-span-2, .col-span-4, .col-span-5, .col-span-7, .col-span-12 {
    grid-column: span 1;
  }
}
</style>
