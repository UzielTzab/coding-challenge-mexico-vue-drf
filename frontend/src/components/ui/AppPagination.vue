<script setup lang="ts">
import { computed } from 'vue';
import AppButton from './AppButton.vue';

interface Props {
  currentPage: number;
  totalItems: number;
  pageSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10
});

const emit = defineEmits<{
  (e: 'page-change', page: number): void
}>();

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.totalItems / props.pageSize));
});

const isFirstPage = computed(() => props.currentPage <= 1);
const isLastPage = computed(() => props.currentPage >= totalPages.value);

const prevPage = () => {
  if (!isFirstPage.value) emit('page-change', props.currentPage - 1);
};

const nextPage = () => {
  if (!isLastPage.value) emit('page-change', props.currentPage + 1);
};

const startItem = computed(() => {
  if (props.totalItems === 0) return 0;
  return (props.currentPage - 1) * props.pageSize + 1;
});

const endItem = computed(() => {
  return Math.min(props.currentPage * props.pageSize, props.totalItems);
});
</script>

<template>
  <div class="pagination-container">
    <div class="pagination-info text-muted">
      Mostrando <strong>{{ startItem }}</strong> - <strong>{{ endItem }}</strong> de <strong>{{ totalItems }}</strong> registros
    </div>
    
    <div class="pagination-controls">
      <AppButton 
        variant="secondary" 
        :disabled="isFirstPage" 
        @click="prevPage"
      >
        <span class="material-symbols-outlined icon-small">chevron_left</span>
        Anterior
      </AppButton>
      
      <span class="page-indicator">Página {{ currentPage }} de {{ totalPages }}</span>
      
      <AppButton 
        variant="secondary" 
        :disabled="isLastPage" 
        @click="nextPage"
      >
        Siguiente
        <span class="material-symbols-outlined icon-small">chevron_right</span>
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-card-soft);
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

.pagination-info {
  font-size: 13px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-indicator {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.icon-small {
  font-size: 20px;
}

@media (max-width: 640px) {
  .pagination-container {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }
  .pagination-controls {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
