<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['back-to-login'])

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!username.value.trim() || !password.value.trim()) {
    errorMessage.value = 'Preencha todos os campos.'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'As senhas não coincidem.'
    return
  }

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/register/`, {
      username: username.value,
      password: password.value
    })

    successMessage.value = response.data.message
    
    username.value = ''
    password.value = ''
    confirmPassword.value = ''

    setTimeout(() => {
      emit('back-to-login')
    }, 2000)

  } catch (error) {
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = 'Erro ao tentar cadastrar. Tente novamente.'
    }
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Criar Conta</h2>
      <p class="subtitle">Cadastre-se para começar a gerenciar suas tarefas</p>

      <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="alert success">{{ successMessage }}</div>

      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label>Usuário</label>
          <input v-model="username" type="text" placeholder="Escolha um nome de usuário" required />
        </div>

        <div class="input-group">
          <label>Senha</label>
          <input v-model="password" type="password" placeholder="Crie uma senha" required />
        </div>

        <div class="input-group">
          <label>Confirmar Senha</label>
          <input v-model="confirmPassword" type="password" placeholder="Digite a senha novamente" required />
        </div>

        <button type="submit" class="auth-btn">Cadastrar</button>
      </form>

      <p class="footer-text">
        Já tem uma conta? 
        <a href="#" @click.prevent="$emit('back-to-login')">Faça Login</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}
.auth-card {
  background: white;
  padding: 30px 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  color: #172b4d;
}
h2 {
  margin-bottom: 10px;
}
.subtitle {
  margin: 0 0 25px 0;
  color: #5e6c84;
  font-size: 0.95rem;
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
  box-shadow: 0 0 0 2px rgba(0, 121, 191, 0.2);
}
.auth-btn {
  width: 100%;
  background-color: #5aac44;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 3px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
}
.auth-btn:hover {
  background-color: #519839;
}
.footer-text {
  text-align: center;
  margin-top: 20px;
  color: #5e6c84;
  font-size: 0.9rem;
}
.footer-text a {
  color: #0079bf;
  text-decoration: none;
  font-weight: 600;
}
.footer-text a:hover {
  text-decoration: underline;
}
.alert {
  padding: 12px;
  border-radius: 3px;
  font-size: 0.9rem;
  margin-bottom: 15px;
  text-align: center;
  font-weight: 500;
}
.alert.error {
  background-color: #ffebe6;
  color: #bf2600;
}
.alert.success {
  background-color: #e6f4ea;
  color: #137333;
}
</style>