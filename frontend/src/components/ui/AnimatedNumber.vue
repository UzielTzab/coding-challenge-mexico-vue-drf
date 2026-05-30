<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  value: number;
  format?: (val: number) => string;
}>();

const direction = ref<'up' | 'down'>('up');
const displayValue = ref(props.value);

watch(() => props.value, (newVal, oldVal) => {
  if (newVal > oldVal) {
    direction.value = 'up';
  } else if (newVal < oldVal) {
    direction.value = 'down';
  }
  displayValue.value = newVal;
});
</script>

<template>
  <div class="animated-number">
    <transition :name="`slide-${direction}`" mode="out-in">
      <span :key="displayValue" class="value-text">
        {{ format ? format(displayValue) : displayValue }}
      </span>
    </transition>
  </div>
</template>

<style scoped>
.animated-number {
  display: inline-flex;
  overflow: hidden;
  position: relative;
  vertical-align: bottom;
}

.value-text {
  display: inline-block;
}

/* Slide UP: numbers go UP (value increases) */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
}
.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}
.slide-up-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

/* Slide DOWN: numbers go DOWN (value decreases) */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
}
.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.slide-down-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
