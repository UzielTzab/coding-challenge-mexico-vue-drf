<script setup lang="ts">
import { computed } from 'vue';
import AppCard from '../ui/AppCard.vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps<{
  data: { pair: string; profit: number }[];
}>();

const chartData = computed(() => {
  const hasData = props.data && props.data.length > 0;
  
  // Mock data temporal si no viene del backend
  const labels = hasData ? props.data.map(d => d.pair) : ['BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'ADA/USD'];
  const dataPoints = hasData ? props.data.map(d => d.profit) : [1200.50, 430.20, 150.00, 85.50, 42.10];

  return {
    labels,
    datasets: [
      {
        label: 'Ganancia Neta',
        data: dataPoints,
        backgroundColor: '#10b981', // var(--color-success)
        borderRadius: 4,
        barThickness: 12,
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y' as const,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#252836',
      titleColor: '#fff',
      bodyColor: '#a0a0b0',
      padding: 10,
      cornerRadius: 4,
      displayColors: false,
      callbacks: {
        label: (context: any) => {
          let label = context.dataset.label || '';
          if (label) label += ': ';
          if (context.parsed.x !== null) {
            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.x);
          }
          return label;
        }
      }
    }
  },
  scales: {
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { display: false }
    },
    y: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#e0e0e0', font: { size: 12, weight: '500' } as any }
    }
  }
};
</script>

<template>
  <AppCard class="chart-card">
    <div class="chart-header">
      <span class="uppercase-label">Ganancia Neta por Par</span>
    </div>
    <div class="chart-container">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </AppCard>
</template>

<style scoped>
.chart-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-header {
  margin-bottom: 16px;
}

.chart-container {
  flex-grow: 1;
  min-height: 200px;
  position: relative;
  width: 100%;
}
</style>
