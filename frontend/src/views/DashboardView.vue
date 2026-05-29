<script setup lang="ts">
import { onMounted } from 'vue';
import { useDashboardSocket } from '../composables/useDashboardSocket';
import KpiCard from '../components/dashboard/KpiCard.vue';
import ExchangeCard from '../components/dashboard/ExchangeCard.vue';
import OpportunityTable from '../components/dashboard/OpportunityTable.vue';
import ExecutionPanel from '../components/dashboard/ExecutionPanel.vue';
import WalletSummary from '../components/dashboard/WalletSummary.vue';
import PerformanceCharts from '../components/dashboard/PerformanceCharts.vue';
import SystemLogPanel from '../components/dashboard/SystemLogPanel.vue';

const { connect } = useDashboardSocket();

onMounted(() => {
  // Iniciar la conexión de WebSockets al cargar el Dashboard
  connect();
});
</script>

<template>
  <div class="dashboard-grid">
    <!-- Fila 1: KPIs (6 cards x 2 columnas = 12 cols) -->
    <KpiCard class="col-span-2" title="P&L Total" value="0.00" prefix="$" />
    <KpiCard class="col-span-2" title="Win Rate" value="0.00" suffix="%" />
    <KpiCard class="col-span-2" title="Ops Ejecutadas" value="0" />
    <KpiCard class="col-span-2" title="Oportunidades" value="0" />
    <KpiCard class="col-span-2" title="Costo Promedio" value="0.00" prefix="$" />
    <KpiCard class="col-span-2" title="Ganancia Neta" value="0.00" prefix="$" />

    <!-- Fila 2: Exchanges (3 cards x 4 columnas = 12 cols) -->
    <ExchangeCard class="col-span-4" exchangeName="Binance" :connected="false" />
    <ExchangeCard class="col-span-4" exchangeName="Kraken" :connected="false" />
    <ExchangeCard class="col-span-4" exchangeName="Bitfinex" :connected="false" />

    <!-- Fila 3: Oportunidades y Ejecución -->
    <OpportunityTable class="col-span-7" />
    <ExecutionPanel class="col-span-5" />

    <!-- Fila 4: Wallets y Charts -->
    <WalletSummary class="col-span-5" />
    <PerformanceCharts class="col-span-7" />

    <!-- Fila 5: Terminal -->
    <SystemLogPanel class="col-span-12" />
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
