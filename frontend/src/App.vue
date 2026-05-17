<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { VueDraggableNext as draggable } from 'vue-draggable-next'

const boards = ref([])
const isLoading = ref(true)
const addingTaskToColumn = ref(null)
const newTaskTitle = ref('')

const activeBoard = computed(() => {
  return boards.value.length > 0 ? boards.value[0] : null
})

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/boards/')
    boards.value = response.data
  } catch (error) {
    console.error("Erro ao buscar a API:", error)
  } finally {
    isLoading.value = false
  }
})

const onDragEnd = async (event) => {
  const taskId = event.item.dataset.taskId
  const newColumnId = event.to.dataset.columnId

  console.log(`Salvando a tarefa ${taskId} na coluna ${newColumnId}...`)

  try {
    await axios.patch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
      column: newColumnId
    })
    console.log("Salvo no banco de dados com sucesso!")
  } catch (error) {
    console.error("Erro ao salvar no banco:", error)
  }
}

const openTaskForm = (columnId) => {
  addingTaskToColumn.value = columnId
  newTaskTitle.value = ''
}

const closeTaskForm = () => {
  addingTaskToColumn.value = null
  newTaskTitle.value = ''
}

const createTask = async (column) => {
  if (!newTaskTitle.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/tasks/', {
      title: newTaskTitle.value,
      description: '', 
      order: 0,
      column: column.id 
    })

    column.tasks.push(response.data)
    
    closeTaskForm()
  } catch (error) {
    console.error("Erro ao criar tarefa:", error)
    alert("Erro ao criar tarefa. Verifique o console.")
  }
}
</script>

<template>
  <main class="app-container">
    <header class="app-header">
      <h1>TaskFlow Pro</h1>
    </header>

    <div v-if="isLoading" class="info-state">
      <p>⏳ Carregando seus quadros...</p>
    </div>
    
    <div v-else-if="activeBoard" class="board-wrapper">
      <h2 class="board-title">{{ activeBoard.name }}</h2>
      
      <div class="board-columns">
        <div v-for="column in activeBoard.columns" :key="column.id" class="column">
          <h3 class="column-title">{{ column.title }}</h3>
          
          <draggable 
            class="task-list" 
            v-model="column.tasks" 
            group="tasks" 
            @end="onDragEnd"
            :data-column-id="column.id"
          >
            <div v-for="task in column.tasks" 
                :key="task.id" 
                class="task-card"
                :data-task-id="task.id"
              >
              {{ task.title }}
            </div>
          </draggable>
          
          <div v-if="addingTaskToColumn === column.id" class="add-task-form">
            <textarea 
              v-model="newTaskTitle"
              placeholder="Insira um título para este cartão..."
              @keyup.enter="createTask(column)"
              autofocus
            ></textarea>
            <div class="add-task-actions">
              <button class="save-btn" @click="createTask(column)">Adicionar cartão</button>
              <button class="cancel-btn" @click="closeTaskForm">✖</button>
            </div>
          </div>
          
          <button v-else class="add-task-btn" @click="openTaskForm(column.id)">
            + Adicionar Tarefa
          </button>
        </div>
      </div>
    </div>
    <div v-else class="info-state">
      <p>Nenhum quadro encontrado. Você precisa criar um no painel Admin ou o servidor do Django está desligado!</p>
    </div>
  </main>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #0079bf;
  color: white;
}
.app-header {
  padding: 10px 20px;
  background-color: rgba(0, 0, 0, 0.2);
}
.board-title {
  padding: 15px 20px;
  font-size: 1.2rem;
}
.board-columns {
  display: flex;
  align-items: flex-start;
  padding: 0 20px;
  gap: 15px;
  overflow-x: auto;
  height: calc(100vh - 120px);
}
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
.add-task-btn {
  width: 100%;
  padding: 8px;
  background: transparent;
  border: none;
  text-align: left;
  color: #5e6c84;
  cursor: pointer;
  border-radius: 3px;
}
.add-task-btn:hover {
  background-color: rgba(9,30,66,0.08);
  color: #172b4d;
}
.empty-state {
  text-align: center;
  margin-top: 50px;
}
.info-state {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
  font-weight: 500;
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