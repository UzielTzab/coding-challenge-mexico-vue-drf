<script setup lang="ts">
import AppCard from '../ui/AppCard.vue';
import AppMetric from '../ui/AppMetric.vue';

interface Props {
  title: string;
  value: string | number;
  variation?: number;
  prefix?: string;
  suffix?: string;
}

defineProps<Props>();
</script>

<template>
  <AppCard>
    <AppMetric 
      :label="title"
      :value="value"
      :variation="variation"
      :prefix="prefix"
      :suffix="suffix"
    />
  </AppCard>
</template>
