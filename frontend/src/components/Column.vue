<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { VueDraggableNext as draggable } from 'vue-draggable-next'
import TaskCard from './TaskCard.vue'

const props = defineProps({
  column: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['task-moved'])

const isAddingTask = ref(false)
const newTaskTitle = ref('')

const openTaskForm = () => {
  isAddingTask.value = true
  newTaskTitle.value = ''
}

const closeTaskForm = () => {
  isAddingTask.value = false
  newTaskTitle.value = ''
}

const createTask = async () => {
  if (!newTaskTitle.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/tasks/', {
      title: newTaskTitle.value,
      description: '', 
      order: 0,
      column: props.column.id 
    })
    
    props.column.tasks.push(response.data)
    closeTaskForm()
  } catch (error) {
    console.error("Erro ao criar tarefa:", error)
  }
}

const onDragEnd = (event) => {
  emit('task-moved', event)
}
</script>

<template>
  <div class="column">
    <h3 class="column-title">{{ column.title }}</h3>
    
    <draggable 
      class="task-list" 
      v-model="column.tasks" 
      group="tasks" 
      @end="onDragEnd"
      :data-column-id="column.id"
    >
      <TaskCard 
        v-for="task in column.tasks" 
        :key="task.id" 
        :task="task" 
        :data-task-id="task.id"
      />
    </draggable>
    
    <div v-if="isAddingTask" class="add-task-form">
      <textarea 
        v-model="newTaskTitle" 
        placeholder="Insira um título para este cartão..." 
        @keyup.enter="createTask" 
        autofocus
      ></textarea>
      <div class="add-task-actions">
        <button class="save-btn" @click="createTask">Adicionar cartão</button>
        <button class="cancel-btn" @click="closeTaskForm">✖</button>
      </div>
    </div>
    
    <button v-else class="add-task-btn" @click="openTaskForm">
      + Adicionar Tarefa
    </button>
  </div>
</template>

<style scoped>
.column {
  background-color: #ebecf0;
  border-radius: 5px;
  width: 280px;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  color: #172b4d;
  max-height: 100%;
}

.column-title {
  padding: 12px;
  font-size: 1rem;
  font-weight: 600;
}

.task-list {
  padding: 0 8px 8px 8px;
  overflow-y: auto;
  min-height: 50px;
}

.add-task-btn {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: none;
  text-align: left;
  color: #5e6c84;
  cursor: pointer;
  border-radius: 0 0 5px 5px;
  font-weight: 500;
}

.add-task-btn:hover {
  background-color: rgba(9,30,66,0.08);
  color: #172b4d;
}

.add-task-form {
  padding: 0 8px 8px 8px;
}

.add-task-form textarea {
  width: 100%;
  border: none;
  border-radius: 3px;
  padding: 8px;
  margin-bottom: 8px;
  box-shadow: 0 1px 0 rgba(9,30,66,0.25);
  font-family: inherit;
  resize: none;
  height: 60px;
}

.add-task-form textarea:focus {
  outline: none;
}

.add-task-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.save-btn {
  background-color: #0079bf;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 500;
}

.save-btn:hover {
  background-color: #026aa7;
}

.cancel-btn {
  background: none;
  border: none;
  color: #6b778c;
  font-size: 1.2rem;
  cursor: pointer;
}

.cancel-btn:hover {
  color: #172b4d;
}
</style>