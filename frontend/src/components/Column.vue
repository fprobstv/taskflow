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
const isEditingTitle = ref(false)
const editTitleText = ref(props.column.title)

const startEditingTitle = () => {
  editTitleText.value = props.column.title
  isEditingTitle.value = true
}

const saveTitle = async () => {
  if (!editTitleText.value.trim() || editTitleText.value === props.column.title) {
    isEditingTitle.value = false
    return
  }

  try {
    await axios.patch(`${import.meta.env.VITE_API_URL}/api/columns/${props.column.id}/`, {
      title: editTitleText.value
    })
    isEditingTitle.value = false
  } catch (error) {
    console.error("Erro ao atualizar título:", error)
  }
}

const deleteColumn = async () => {
  if (confirm("ATENÇÃO: Deseja mesmo excluir esta lista e TODAS as tarefas nela?")) {
    try {
      await axios.delete(`${import.meta.VITE_API_URL}/api/columns/${props.column.id}/`)
    } catch (error) {
      console.error("Erro ao deletar coluna:", error)
    }
  }
}

const openTaskForm = () => {
  isAddingTask.value = true
  newTaskTitle.value = ''
}

const closeTaskForm = () => {
  isAddingTask.value = false
  newTaskTitle.value = ''
}

const createTask = async () => {
  const token = localStorage.getItem('access_token')
  if (!newTaskTitle.value.trim()) return

  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/api/tasks/`, {
      title: newTaskTitle.value,
      description: '', 
      order: 0,
      column: props.column.id 
    }, {
        headers: { Authorization: `Bearer ${token}` }
      }
  )
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
    
    <div class="column-header">
      <input 
        v-if="isEditingTitle" 
        v-model="editTitleText" 
        class="edit-title-input"
        @keyup.enter="saveTitle"
        @blur="saveTitle"
        autofocus
      />
      <h3 v-else class="column-title" @click="startEditingTitle" title="Clique para editar">
        {{ column.title }}
      </h3>
      <button class="delete-btn" @click="deleteColumn" title="Deletar lista">❌</button>
    </div>
    
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
.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px 0 12px;
}
.column-title {
  cursor: pointer;
  border-radius: 3px;
  padding: 4px 8px;
  margin: 0;
  flex-grow: 1;
  font-size: 1rem;
  font-weight: 600;
}
.column-title:hover {
  background-color: rgba(9,30,66,0.08);
}
.edit-title-input {
  flex-grow: 1;
  font-size: 1rem;
  font-weight: 600;
  padding: 4px 8px;
  border: 2px solid #0079bf;
  border-radius: 3px;
  font-family: inherit;
  margin-right: 5px;
}
.edit-title-input:focus {
  outline: none;
}
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0; 
  transition: opacity 0.2s, transform 0.2s;
  font-size: 1rem;
  padding: 4px;
}
.column-header:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  transform: scale(1.2);
}
.task-list {
  padding: 8px;
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
  box-sizing: border-box;
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