<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  console.log("1. Botão clicado! Tentando logar com:", username.value) 
  errorMessage.value = ''
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/token/', {
      username: username.value,
      password: password.value
    })
    
    console.log("2. Sucesso! O Django devolveu os tokens:", response.data) 
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    
    emit('login-success')
  } catch (error) {
    console.error("3. Erro no login:", error) 
    errorMessage.value = 'Usuário ou senha incorretos.'
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Entrar no TaskFlow</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Usuário</label>
          <input type="text" v-model="username" required autofocus />
        </div>
        
        <div class="input-group">
          <label>Senha</label>
          <input type="password" v-model="password" required />
        </div>
        
        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        
        <button type="submit" class="login-btn">Entrar</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container { 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 80vh; 
}
.login-box { 
    background: white; 
    padding: 30px 40px; 
    border-radius: 8px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
    width: 100%; 
    max-width: 400px; 
    text-align: center; 
    color: #172b4d;
}
.input-group { 
    margin-bottom: 15px; 
    text-align: left; 
}
.input-group label { 
    display: block; 
    font-weight: 600; 
    color: #5e6c84; 
    margin-bottom: 5px; 
    font-size: 0.9rem; 
}
.input-group input { 
    width: 100%; 
    box-sizing: border-box; 
    padding: 10px; 
    border: 2px solid #dfe1e6; 
    border-radius: 3px; 
    font-size: 1rem; 
}
.input-group input:focus { 
    outline: none; 
    border-color: #0079bf; 
}
.error-msg { 
    color: #eb5a46; 
    font-size: 0.9rem; 
    margin-bottom: 15px; 
    font-weight: bold; 
}
.login-btn { 
    width: 100%; 
    background-color: #0079bf; 
    color: white; 
    border: none; 
    padding: 12px; 
    border-radius: 3px; 
    font-size: 1rem; 
    font-weight: bold; 
    cursor: pointer; 
}
.login-btn:hover { 
    background-color: #026aa7; 
}
</style>