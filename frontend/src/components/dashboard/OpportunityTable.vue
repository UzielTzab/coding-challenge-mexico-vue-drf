<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AppCard from '../ui/AppCard.vue';
import { getOpportunities } from '../../services/opportunities.service';
import { useFormatters } from '../../composables/useFormatters';

const opportunities = ref<any[]>([]);
const { formatUSD, formatPercent } = useFormatters();

onMounted(async () => {
  try {
    const data = await getOpportunities();
    const results = data.results || data;
    opportunities.value = Array.isArray(results) ? results.slice(0, 5) : []; // show top 5
  } catch (error) {
    console.error('Error fetching opportunities:', error);
  }
});
</script>

<template>
  <AppCard class="opp-card" variant="soft">
    <div class="opp-header">
      <h3>Oportunidades en Tiempo Real</h3>
    </div>
    <div class="table-container">
      <table class="opps-table">
        <thead>
          <tr>
            <th>Par</th>
            <th>Buy</th>
            <th>Sell</th>
            <th>Spread</th>
            <th>Profit Neto</th>
          </tr>
        </thead>
        <tbody v-if="opportunities.length > 0">
          <tr v-for="opp in opportunities" :key="opp.id">
            <td>{{ opp.symbol }}</td>
            <td>{{ opp.buy_exchange }}</td>
            <td>{{ opp.sell_exchange }}</td>
            <td class="text-success">{{ formatPercent(opp.spread_percent || 0) }}</td>
            <td class="text-success">{{ formatUSD(opp.net_profit || 0) }}</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="5" class="empty-state">No hay oportunidades recientes</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppCard>
</template>

<style scoped>
.opp-card { display: flex; flex-direction: column; height: 100%; background-color: var(--color-bg-base); }
.opp-header { margin-bottom: 16px; }
.opp-header h3 { margin: 0; font-size: 16px; }
.table-container { overflow-x: auto; }
.opps-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.opps-table th { text-align: left; padding: 12px 8px; color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border); font-weight: 500; }
.opps-table td { padding: 12px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.empty-state { text-align: center; padding: 40px; color: var(--color-text-muted); font-size: 14px; }
</style>
