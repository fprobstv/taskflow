<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Board from './components/Board.vue'

const boards = ref([])
const isLoading = ref(true) 

const activeBoard = computed(() => {
  return boards.value.length > 0 ? boards.value[0] : null
})

const fetchBoards = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/boards/')
    boards.value = response.data
  } catch (error) {
    console.error("Erro ao buscar a API:", error)
  }
}

onMounted(async () => {
  await fetchBoards()
  isLoading.value = false

  const ws = new WebSocket('ws://127.0.0.1:8081/ws')

  ws.onopen = () => {
    console.log("Conectado ao WebSocket do Goland com sucesso!")
  }

  ws.onmessage = (event) => {
    console.log("Aviso do Go recebido:", event.data)
    fetchBoards()
  }
})

const onDragEnd = async (event) => {
  const taskId = event.item.dataset.taskId
  const newColumnId = event.to.dataset.columnId
  try {
    await axios.patch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, { column: newColumnId })
  } catch (error) {
    console.error("Erro ao salvar no banco:", error)
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
    
    <Board 
      v-else-if="activeBoard" 
      :board="activeBoard" 
      @task-moved="onDragEnd" 
    />
    
    <div v-else class="info-state">
      <p>❌ Nenhum quadro encontrado. Você precisa criar um no painel Admin ou o servidor do Django está desligado!</p>
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
.info-state { 
  text-align: center; 
  margin-top: 50px; 
  font-size: 1.2rem; 
  font-weight: 500; 
}
</style>
<style>
body {
  margin: 0;
  padding: 0;
  background-color: #0079bf; 
}
</style>