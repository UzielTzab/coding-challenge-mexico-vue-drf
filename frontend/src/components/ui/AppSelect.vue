<script setup lang="ts">
interface Option {
  value: string | number;
  label: string;
}

interface Props {
  modelValue: string | number;
  label?: string;
  options: Option[];
  disabled?: boolean;
}

defineProps<Props>();
defineEmits(['update:modelValue']);
</script>

<template>
  <div class="app-select-group">
    <label v-if="label" class="app-label">{{ label }}</label>
    <select 
      :value="modelValue"
      :disabled="disabled"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      class="app-select"
    >
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.app-select-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.app-label {
  font-size: var(--text-sm, 14px);
  color: var(--color-text-secondary);
  font-weight: 500;
}

.app-select {
  height: 40px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm, 8px);
  padding: 0 12px;
  color: var(--color-text-primary);
  transition: 160ms ease;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23A8B0C3%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 12px top 50%;
  background-size: 10px auto;
}

.app-select:focus {
  outline: none;
  border-color: var(--color-primary-light);
  box-shadow: 0 0 0 2px rgba(126, 176, 243, 0.2);
}

.app-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.app-select option {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
}
</style>
