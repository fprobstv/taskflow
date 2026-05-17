<script setup>
defineProps({
  task: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="task-card">
    {{ task.title }}
  </div>
</template>

<style scoped>
.task-card {
  background-color: white;
  border-radius: 3px;
  padding: 10px;
  margin-bottom: 8px;
  box-shadow: 0 1px 0 rgba(9,30,66,0.25);
  cursor: grab;
  font-size: 0.9rem;
}

.task-card:active {
  cursor: grabbing;
}

.task-card:hover {
  background-color: #f4f5f7;
}
</style>