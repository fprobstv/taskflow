<script setup>
import { ref } from 'vue' 
import axios from 'axios'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const isEditing = ref(false)
const editTitle = ref(props.task.title)

const startEditing = () => {
  editTitle.value = props.task.title
  isEditing.value = true
}

const saveTitle = async () => {
  // Cancela se estiver vazio ou igual
  if (!editTitle.value.trim() || editTitle.value === props.task.title) {
    isEditing.value = false
    return
  }

  try {
    await axios.patch(`http://127.0.0.1:8000/api/tasks/${props.task.id}/`, {
      title: editTitle.value
    })
    isEditing.value = false
  } catch (error) {
    console.error("Erro ao atualizar tarefa:", error)
  }
}

const deleteTask = async () => {
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/tasks/${props.task.id}/`)
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error)
    }
  }
}
</script>

<template>
  <div class="task-card">
    
    <input 
      v-if="isEditing" 
      v-model="editTitle" 
      class="edit-task-input"
      @keyup.enter="saveTitle"
      @blur="saveTitle"
      autofocus
    />
    
    <span 
      v-else 
      class="task-title" 
      @click="startEditing" 
      title="Clique para editar"
    >
      {{ task.title }}
    </span>
    
    <button class="delete-btn" @click="deleteTask" title="Deletar tarefa">❌</button>
  </div>
</template>

<style scoped>
.task-card {
  background-color: white;
  padding: 10px;
  border-radius: 3px;
  box-shadow: 0 1px 0 rgba(9,30,66,0.25);
  margin-bottom: 8px;
  cursor: grab;
  font-size: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px; 
}
.task-card:active {
  cursor: grabbing;
}

.task-title {
  flex-grow: 1;
  cursor: pointer;
  padding: 4px;
  border-radius: 3px;
  word-break: break-word; 
}
.task-title:hover {
  background-color: rgba(9,30,66,0.08);
}

.edit-task-input {
  flex-grow: 1;
  font-size: 0.9rem;
  padding: 3px 4px;
  border: 2px solid #0079bf;
  border-radius: 3px;
  font-family: inherit;
  width: 100%;
}
.edit-task-input:focus {
  outline: none;
}
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0; 
  transition: opacity 0.2s, transform 0.2s;
  font-size: 1rem;
  padding: 0; 
}
.task-card:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  transform: scale(1.2);
}
</style>