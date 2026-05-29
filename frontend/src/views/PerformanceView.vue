<script setup lang="ts">
import { ref, onMounted } from 'vue';
import MetricCard from '../components/performance/MetricCard.vue';
import PnlLineChart from '../components/performance/PnlLineChart.vue';
import ProfitByPairBarChart from '../components/performance/ProfitByPairBarChart.vue';
import OpportunityStatusDonut from '../components/performance/OpportunityStatusDonut.vue';
import api from '../services/http'; // Para el endpoint de analytics
import { useFormatters } from '../composables/useFormatters';

const { formatUSD } = useFormatters();

const isLoading = ref(true);

interface Analytics {
  global_pnl: number;
  global_win_rate: number;
  trades_count: number;
  pnl_history: any[];
  profit_by_pair: any[];
  status_stats: { executed: number; failed: number; discarded: number; };
}

const analytics = ref<Analytics>({
  global_pnl: 0,
  global_win_rate: 0,
  trades_count: 0,
  pnl_history: [],
  profit_by_pair: [],
  status_stats: { executed: 0, failed: 0, discarded: 0 }
});

const loadAnalytics = async () => {
  try {
    const { data } = await api.get('/api/analytics/performance/');
    analytics.value = data;
  } catch (error) {
    console.error('Error fetching performance:', error);
    // Mock temporal para visualización
    analytics.value = {
      global_pnl: 1540.50,
      global_win_rate: 85,
      trades_count: 142,
      pnl_history: [],
      profit_by_pair: [{ pair: 'BTC/USD', profit: 1200 }, { pair: 'ETH/USD', profit: 340.5 }],
      status_stats: { executed: 120, failed: 12, discarded: 10 }
    };
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadAnalytics();
});
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Rendimiento y Analíticas</h2>
      <p class="text-muted">Métricas de rentabilidad histórica y eficacia del motor.</p>
    </div>
    
    <div v-if="!isLoading" class="dashboard-grid">
      <!-- Metrics Row -->
      <div class="metrics-row">
        <MetricCard 
          title="Ganancia Neta (P&L)" 
          :value="'+' + formatUSD(analytics.global_pnl)" 
          trend="up" 
          trendValue="+12% (30d)" 
        />
        <MetricCard 
          title="Tasa de Éxito" 
          :value="analytics.global_win_rate + '%'" 
          trend="neutral" 
          trendValue="Estable" 
        />
        <MetricCard 
          title="Operaciones Totales" 
          :value="analytics.trades_count" 
        />
      </div>

      <!-- Charts Row 1 -->
      <div class="charts-main">
        <div class="main-chart">
          <PnlLineChart :data="analytics.pnl_history" />
        </div>
        <div class="side-chart">
          <OpportunityStatusDonut :stats="analytics.status_stats" />
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="charts-bottom">
        <div class="half-chart">
          <ProfitByPairBarChart :data="analytics.profit_by_pair" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.view-header h2 { margin: 0 0 8px 0; }
.view-header p { margin: 0; }

.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.charts-main {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  min-height: 300px;
}

.charts-bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
</style>
