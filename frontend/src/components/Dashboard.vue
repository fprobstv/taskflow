<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['select-board'])

const boards = ref([])
const newBoardName = ref('')
const isCreating = ref(false)

const fetchMyBoards = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/boards/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    boards.value = response.data
  } catch (error) {
    console.error("Erro ao buscar seus quadros:", error)
  }
}

const createBoard = async () => {
  if (!newBoardName.value.trim()) return
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.post('http://127.0.0.1:8000/api/boards/', 
      { name: newBoardName.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    boards.value.push(response.data)
    newBoardName.value = ''
    isCreating.value = false
  } catch (error) {
    console.error("Erro ao criar quadro:", error)
  }
}

onMounted(() => {
  fetchMyBoards()
})
</script>

<template>
  <div class="dashboard-container">
    <h2>Meus Quadros de Trabalho</h2>
    
    <div class="boards-grid">
      <div 
        v-for="board in boards" 
        :key="board.id" 
        class="board-card"
        @click="emit('select-board', board.id)"
      >
        <h3>{{ board.name }}</h3>
      </div>

      <div v-if="!isCreating" class="board-card add-board" @click="isCreating = true">
        <h3>+ Criar novo quadro</h3>
      </div>

      <div v-else class="board-card create-form">
        <input 
          v-model="newBoardName" 
          type="text" 
          placeholder="Título do quadro..." 
          @keyup.enter="createBoard"
          autofocus
        />
        <div class="form-actions">
          <button class="save-btn" @click="createBoard">Criar</button>
          <button class="cancel-btn" @click="isCreating = false">✖</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: #172b4d; 
}
h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
  font-weight: 600;
  color: #172b4d;
}
.boards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.board-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  height: 100px;
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: 1px solid #dfe1e6;
}
.board-card:hover {
  background: #f4f5f7;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
.board-card h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  word-break: break-word;
  color: #172b4d;
}
.add-board {
  background: #f4f5f7;
  border: 2px dashed #c1c7d0;
  justify-content: center;
  align-items: center;
}
.add-board h3 {
  color: #5e6c84;
  font-weight: 500;
}
.add-board:hover {
  background: #e9ebf0;
  border-color: #a5adba;
}
.create-form {
  flex-direction: column;
  gap: 10px;
  background: white;
  cursor: default;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
.create-form:hover {
  background: white;
  transform: none;
}
.create-form input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: 2px solid #dfe1e6;
  border-radius: 3px;
  font-size: 1rem;
}
.create-form input:focus {
  outline: none;
  border-color: #0079bf;
  box-shadow: 0 0 0 2px rgba(0, 121, 191, 0.2);
}
.form-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}
.save-btn {
  background-color: #0079bf;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 3px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
}
.save-btn:hover {
  background-color: #026aa7;
}
.cancel-btn {
  background: none;
  border: none;
  color: #6b778c;
  cursor: pointer;
  font-size: 1.4rem;
  padding: 0 5px;
  line-height: 1;
}
.cancel-btn:hover {
  color: #172b4d;
}
</style>