<script setup lang="ts">
import { ref } from 'vue';
import AppCard from '../components/ui/AppCard.vue';
import AppInput from '../components/ui/AppInput.vue';
import AppButton from '../components/ui/AppButton.vue';

const maxSpread = ref('0.5');
const minProfit = ref('1.0');
</script>

<template>
  <div class="view-container">
    <div class="view-header">
      <h2>Configuración</h2>
      <p class="text-muted">Ajustes del motor de arbitraje.</p>
    </div>
    
    <AppCard class="settings-card">
      <div class="form-group">
        <AppInput label="Spread Máximo Permitido (%)" v-model="maxSpread" type="number" />
        <AppInput label="Ganancia Mínima Esperada (USD)" v-model="minProfit" type="number" />
      </div>
      <div class="actions">
        <AppButton variant="primary">Guardar Cambios</AppButton>
      </div>
    </AppCard>
  </div>
</template>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 600px;
}
.view-header h2 { margin: 0 0 8px 0; }
.view-header p { margin: 0; }
.settings-card { padding: 32px; }
.form-group { display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px; }
.actions { display: flex; justify-content: flex-end; }
</style>
