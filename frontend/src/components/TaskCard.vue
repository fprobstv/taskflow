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
const token = localStorage.getItem('access_token')

const startEditing = () => {
  editTitle.value = props.task.title
  isEditing.value = true
}

const saveTitle = async () => {
  if (!editTitle.value.trim() || editTitle.value === props.task.title) {
    isEditing.value = false
    return
  }

  try {
    await axios.patch(`${import.meta.env.VITE_API_URL}/api/tasks/${props.task.id}/`, {
      title: editTitle.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    isEditing.value = false
  } catch (error) {
    console.error("Erro ao atualizar tarefa:", error)
  }
}

const deleteTask = async () => {
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/api/tasks/${props.task.id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error)
    }
  }
}

const isModalOpen = ref(false)
const editDescription = ref(props.task.description || '')

const openModal = () => {
  editDescription.value = props.task.description || ''  
  isModalOpen.value = true 
}

const closeModal = () => {
  isModalOpen.value = false
}

const saveDescription = async () => {
  try {
    await axios.patch(`${import.meta.env.VITE_API_URL}/api/tasks/${props.task.id}/`, {
      description: editDescription.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    closeModal()
  } catch (error) {
    console.error("Erro ao salvar descrição:", error)
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
    
    <span v-else class="task-title" @click="startEditing" title="Clique para editar o título">
      {{ task.title }}
      <span v-if="task.description" class="has-desc-icon" title="Esta tarefa tem uma descrição">≡</span>
    </span>
    
    <div class="card-actions">
      <button class="icon-btn" @click.stop="openModal" title="Abrir detalhes">📝</button>
      <button class="icon-btn delete-btn" @click.stop="deleteTask" title="Deletar tarefa">❌</button>
    </div>

    <Teleport to="body">
      <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          
          <div class="modal-header">
            <h2>{{ task.title }}</h2>
            <button class="close-modal-btn" @click="closeModal">✖</button>
          </div>
          
          <div class="modal-body">
            <label class="desc-label">Descrição:</label>
            <textarea 
              v-model="editDescription" 
              class="desc-textarea" 
              placeholder="Adicione uma descrição mais detalhada..."
            ></textarea>
            
            <div class="modal-footer">
              <button class="save-btn" @click="saveDescription">Salvar Descrição</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
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
.has-desc-icon {
  color: #5e6c84;
  margin-left: 5px;
  font-weight: bold;
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
.card-actions {
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.2s;
}
.task-card:hover .card-actions {
  opacity: 1;
}
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  transition: transform 0.2s;
}
.icon-btn:hover {
  transform: scale(1.2);
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start; 
  padding-top: 10vh;
  z-index: 1000; 
  cursor: default;
}
.modal-content {
  background-color: #f4f5f7;
  width: 90%;
  max-width: 600px;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 20px 10px 20px;
}
.modal-header h2 {
  margin: 0;
  color: #172b4d;
  font-size: 1.2rem;
}
.close-modal-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #6b778c;
}
.close-modal-btn:hover {
  color: #172b4d;
}
.modal-body {
  padding: 10px 20px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.desc-label {
  font-weight: 600;
  color: #172b4d;
  font-size: 1rem;
}
.desc-textarea {
  width: 100%;
  box-sizing: border-box;
  min-height: 100px;
  padding: 10px;
  border-radius: 3px;
  border: 1px solid #dfe1e6;
  font-family: inherit;
  font-size: 0.9rem;
  resize: vertical;
  background-color: #fafbfc;
}
.desc-textarea:focus {
  outline: none;
  border-color: #0079bf;
  background-color: white;
}
.modal-footer {
  margin-top: 10px;
  display: flex;
  justify-content: flex-start;
}
.save-btn {
  background-color: #0079bf;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 500;
}
.save-btn:hover {
  background-color: #026aa7;
}
</style>