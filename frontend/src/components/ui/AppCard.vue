<script setup lang="ts">
interface Props {
  variant?: 'default' | 'soft' | 'highlighted' | 'terminal';
}

withDefaults(defineProps<Props>(), {
  variant: 'default'
});
</script>

<template>
  <div :class="['app-card', `app-card--${variant}`]">
    <slot></slot>
  </div>
</template>

<style scoped>
.app-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg, 16px);
  padding: 20px;
}

.app-card--soft {
  background: var(--color-bg-card-soft);
}

.app-card--highlighted {
  border-color: rgba(126, 176, 243, 0.65);
  box-shadow: 0 0 24px rgba(68, 81, 187, 0.25);
}

.app-card--terminal {
  background: var(--color-bg-terminal);
  font-family: var(--font-mono, monospace);
}
</style>
