<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Column from './Column.vue'

const props = defineProps({
  board: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['task-moved'])

const isAddingColumn = ref(false)
const newColumnTitle = ref('')
const isShareModalOpen = ref(false)
const guestUsername = ref('')

const createColumn = async () => {
  const token = localStorage.getItem('access_token')
  if (!newColumnTitle.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/columns/', {
      title: newColumnTitle.value,
      board: props.board.id,
      order: props.board.columns.length
    },  {
      headers: { Authorization: `Bearer ${token}` }
    }
    )

    const novaColuna = response.data
    if (!novaColuna.tasks) novaColuna.tasks = []

    props.board.columns.push(novaColuna)
    
    isAddingColumn.value = false
    newColumnTitle.value = ''
  } catch (error) {
    console.error("Erro ao criar coluna:", error)
    alert("Erro ao criar coluna. Verifique o console do navegador.")
  }
}

const shareBoard = async () => {
  const username = guestUsername.value.trim()
  if (!username) return

  const token = localStorage.getItem('access_token')

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/boards/${props.board.id}/share/`, 
      { username: username },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert(response.data.message) 
    
    guestUsername.value = ''
    isShareModalOpen.value = false
  } catch (error) {
    console.error("Erro ao compartilhar quadro:", error)
    
    if (error.response && error.response.data && error.response.data.error) {
      alert(error.response.data.error)
    } else {
      alert("Erro ao tentar compartilhar o quadro. Verifique o console.")
    }
  }
}
</script>

<template>
  <div class="board-wrapper">

    <div class="board-header-top">
      <h2 class="board-title">{{ board.name }}</h2>
      <button class="share-btn" @click="isShareModalOpen = true">Compartilhar</button>
    </div>

    <div class="board-columns">
      
      <Column 
        v-for="column in board.columns" 
        :key="column.id" 
        :column="column" 
        @task-moved="$emit('task-moved', $event)"
      />

      <div class="column add-column-wrapper">
        <div v-if="isAddingColumn" class="add-column-form">
          <input 
            v-model="newColumnTitle" 
            type="text" 
            placeholder="Insira o título da lista..." 
            @keyup.enter="createColumn"
            autofocus
          />
          <div class="add-column-actions">
            <button class="save-btn" @click="createColumn">Adicionar lista</button>
            <button class="cancel-btn" @click="isAddingColumn = false">✖</button>
          </div>
        </div>
        <button v-else class="add-column-btn" @click="isAddingColumn = true">
          + Adicionar outra lista
        </button>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="isShareModalOpen" class="modal-overlay" @click.self="isShareModalOpen = false">
        <div class="modal-content share-modal">
          <div class="modal-header">
            <h2>Compartilhar Quadro</h2>
            <button class="close-modal-btn" @click="isShareModalOpen = false">✖</button>
          </div>
          
          <div class="modal-body">
            <p class="share-desc">Digite o nome de usuário da pessoa que você deseja convidar para editar este quadro com você.</p>
            <input 
              v-model="guestUsername" 
              type="text" 
              class="share-input" 
              placeholder="Nome de usuário (ex: joao123)"
              @keyup.enter="shareBoard"
              autofocus
            />
            <div class="modal-footer">
              <button class="save-btn share-submit-btn" @click="shareBoard">Enviar Convite</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.board-wrapper {
  padding: 20px;
  height: calc(100vh - 61px); /* Altura total - altura do header */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.board-header-top {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding: 0 10px;
}

.board-title { 
  margin: 0;
  font-size: 1.6rem; 
  font-weight: 600;
  color: #172b4d; 
}

.share-btn {
  background-color: #f4f5f7;
  color: #172b4d;
  border: 1px solid #dfe1e6;
  padding: 6px 12px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background-color 0.2s, border-color 0.2s;
}

.share-btn:hover {
  background-color: #e9ebf0;
  border-color: #c1c7d0;
}

.board-columns {
  display: flex;
  align-items: flex-start;
  gap: 15px; 
  overflow-x: auto; 
  flex-grow: 1;
  padding: 10px;
}

.column { 
  background-color: #ebecf0; 
  border-radius: 8px; 
  width: 280px; 
  min-width: 280px; 
  display: flex; 
  flex-direction: column; 
  color: #172b4d; 
  max-height: 100%; 
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.add-column-wrapper { 
  background-color: #e9ebf0;
  border-radius: 8px;
}

.add-column-btn { 
  width: 100%; 
  padding: 12px; 
  background: transparent; 
  border: none; 
  text-align: left; 
  color: #5e6c84; 
  font-weight: 500; 
  font-size: 0.95rem; 
  cursor: pointer; 
  border-radius: 8px; 
}

.add-column-btn:hover { 
  background-color: #dfe1e6; 
}

.add-column-form { 
  padding: 8px; 
  background-color: #ebecf0; 
  border-radius: 8px; 
}

.add-column-form input { 
  width: 100%;
  border: 2px solid #dfe1e6; 
  border-radius: 3px; 
  padding: 10px; 
  margin-bottom: 8px; 
  font-size: 0.9rem; 
  box-sizing: border-box;
}

.add-column-form input:focus { 
  outline: none; 
  border-color: #0079bf;
}

.add-column-actions { 
  display: flex; 
  align-items: center; 
  gap: 10px; 
}

.save-btn { 
  background-color: #0079bf; 
  color: white; 
  border: none; 
  padding: 8px 16px;
  border-radius: 3px; 
  cursor: pointer; 
  font-weight: bold;
  font-size: 0.9rem;
}

.save-btn:hover { 
  background-color: #026aa7; 
}

.add-column-form .cancel-btn { 
  color: #6b778c; 
  background: none; 
  border: none; 
  font-size: 1.4rem; 
  cursor: pointer; 
  padding: 0 5px;
  line-height: 1;
}

.add-column-form .cancel-btn:hover { 
  color: #172b4d; 
}

/* Estilos do Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: flex-start; 
  padding-top: 15vh; z-index: 1000;
}

.modal-content {
  background-color: #f4f5f7;
  width: 90%; max-width: 450px;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dfe1e6;
}

.modal-header h2 { 
  margin: 0; 
  color: #172b4d; 
  font-size: 1.2rem; 
  font-weight: 600;
}

.close-modal-btn { 
  background: none; 
  border: none; 
  font-size: 1.4rem; 
  cursor: pointer; 
  color: #6b778c; 
  padding: 0 5px;
  line-height: 1;
}

.close-modal-btn:hover { color: #172b4d; }

.modal-body { 
  padding: 20px; 
  display: flex; 
  flex-direction: column; 
  gap: 15px; 
}

.share-desc { 
  margin: 0; 
  color: #5e6c84; 
  font-size: 0.95rem; 
  line-height: 1.4; 
}

.share-input {
  width: 100%; 
  box-sizing: border-box;
  padding: 10px;
  border: 2px solid #dfe1e6;
  border-radius: 3px;
  font-size: 1rem;
}

.share-input:focus { 
  border-color: #0079bf; 
  outline: none; 
  box-shadow: 0 0 0 2px rgba(0, 121, 191, 0.2);
}

.modal-footer {
  margin-top: 10px;
}

.share-submit-btn { 
  width: 100%; 
  padding: 10px; 
  font-size: 1rem; 
}
</style>