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

const createColumn = async () => {
  if (!newColumnTitle.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/columns/', {
      title: newColumnTitle.value,
      board: props.board.id,
      order: props.board.columns.length
    })

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
</script>

<template>
  <div class="board-wrapper">
    <h2 class="board-title">{{ board.name }}</h2>
    
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
  </div>
</template>

<style scoped>
.board-wrapper {
  background: linear-gradient(135deg, #0079bf, #5067c5);
  min-height: 100vh;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.columns-container {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  overflow-x: auto; 
  padding-bottom: 20px; 
  height: calc(100vh - 80px); 
}
.board-title { 
  padding: 15px 20px; 
  font-size: 1.2rem; 
  color: white; 
  margin-top: 0;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2); 
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
.add-column-wrapper { 
    background-color: rgba(255, 255, 255, 0.24); 
    color: white; 
}
.add-column-btn { 
    width: 100%; 
    padding: 12px; 
    background: transparent; 
    border: none; 
    text-align: left; 
    color: white; 
    font-weight: 600; 
    font-size: 1rem; 
    cursor: pointer; 
    border-radius: 5px; 
}
.add-column-btn:hover { 
    background-color: rgba(0, 0, 0, 0.1); 
}
.add-column-form { 
    padding: 8px; 
    background-color: #ebecf0; 
    border-radius: 5px; 
}
.add-column-form input { 
    width: 100%;
    border: 2px solid #0079bf; 
    border-radius: 3px; 
    padding: 8px; 
    margin-bottom: 8px; 
    font-family: inherit; 
    font-size: 0.9rem; 
}
.add-column-form input:focus { 
    outline: none; 
}
.add-column-form .cancel-btn { 
    color: #6b778c; 
    background: none; 
    border: none; 
    font-size: 1.2rem; 
    cursor: pointer; 
}
.add-column-form .cancel-btn:hover { 
    color: #172b4d; 
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
    padding: 6px 12px; 
    border-radius: 3px; 
    cursor: pointer; 
    font-weight: 500; 
}
.save-btn:hover { 
    background-color: #026aa7; 
}
</style>