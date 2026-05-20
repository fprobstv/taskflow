<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Board from './components/Board.vue'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'

const boardData = ref(null)
const isAuthenticated = ref(false) 
const isLoading = ref(true)
const currentBoardId = ref(null)

const fetchBoards = async () => {
  if (!currentBoardId.value) return
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get(`http://127.0.0.1:8000/api/boards/${currentBoardId.value}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    boardData.value = response.data
  } catch (error) {
    console.error("Erro ao buscar o quadro:", error)
    if (error.response && error.response.status === 401) {
      handleLogout()
    }
  }
}

const onDragEnd = async (event) => {
  const taskId = event.item.dataset.taskId
  const newColumnId = event.to.dataset.columnId
  const token = localStorage.getItem('access_token')
  
  try {
    await axios.patch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, 
      { column: newColumnId },
      { headers: { Authorization: `Bearer ${token}` } }
    )
  } catch (error) {
    console.error("Erro ao salvar no banco:", error)
  }
}

const handleLoginSuccess = () => {
  isAuthenticated.value = true
  fetchBoards()
  connectWebSocket() 
}

const handleSelectBoard = (boardId) => {
  currentBoardId.value = boardId
  fetchBoards()
}

const handleBackToDashboard = () => {
  currentBoardId.value = null
  boardData.value = null 
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isAuthenticated.value = false
  boardData.value = null
}

const connectWebSocket = () => {
  const ws = new WebSocket('ws://127.0.0.1:8081/ws')
  ws.onopen = () => console.log("Conectado ao WebSocket do Golang!")
  ws.onmessage = () => fetchBoards()
}

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isAuthenticated.value = true
    await fetchBoards()
    connectWebSocket()
  }
  isLoading.value = false
})
</script>

<template>
  <main class="app-container">
    <header class="app-header">
      <h1>TaskFlow Pro</h1>
      <div v-if="isAuthenticated" class="header-actions">
        <button v-if="currentBoardId" class="nav-btn" @click="handleBackToDashboard">📁 Meus Quadros</button>
        <button class="logout-btn" @click="handleLogout">Sair</button>
      </div>
    </header>

    <div v-if="isLoading" class="info-state">
      <p>⏳ Carregando o sistema...</p>
    </div>

    <Login v-else-if="!isAuthenticated" @login-success="handleLoginSuccess" />
    
    <div v-else class="authenticated-area">
      
      <Dashboard v-if="!currentBoardId" @select-board="handleSelectBoard" />

      <Board 
        v-else-if="boardData" 
        :board="boardData" 
        @task-moved="onDragEnd" 
      />
      
      <div v-else class="info-state">
        <p>❌ Erro ao carregar as informações deste quadro. Verifique se ele existe.</p>
      </div>

    </div>
  </main>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.app-header {
  padding: 10px 20px;
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dfe1e6;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.app-header h1 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 600;
  color: #172b4d;
}
.header-actions {
  display: flex;
  gap: 15px;
}
.info-state {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
  font-weight: 500;
  color: #5e6c84;
}
.logout-btn, .nav-btn {
  background-color: #f4f5f7;
  color: #172b4d;
  border: 1px solid #dfe1e6;
  padding: 8px 16px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background-color 0.2s, border-color 0.2s;
}
.logout-btn:hover, .nav-btn:hover {
  background-color: #e9ebf0;
  border-color: #c1c7d0;
}
</style>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: #f4f5f7; 
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>