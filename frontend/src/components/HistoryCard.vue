<script setup lang="ts">
defineProps<{ message: string }>()

</script>

<template>
<div class="history-card">
  <div class="suggestion">{{message}}</div>
</div>
</template>

<style scoped>
.history-card {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s;
}

.history-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.history-time {
  font-size: 12px;
  color: #888;
  margin-bottom: 6px;
}

.history-query {
  font-weight: 500;
  margin-bottom: 6px;
  font-size: 1rem;
  color: #333;
}

.suggestion {
  font-size: 14px;
  color: #007acc;
  line-height: 1.4;
}
</style>