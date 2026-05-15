# TaskFlow

> Plataforma Kanban em tempo real construída com Django, Vue.js, Go e Docker.

## 🚀 Tecnologias

- Django REST Framework
- Vue.js 3
- Golang (WebSockets)
- PostgreSQL
- Redis
- Elasticsearch
- Docker Compose

---

## ✨ Funcionalidades

- Autenticação JWT
- Boards e colunas Kanban
- Drag-and-drop de tarefas
- Atualização em tempo real entre diferentes usuários
- Busca inteligente com Elasticsearch

---

## 🧠 Arquitetura

```text
Vue.js → Django API → PostgreSQL
                 ↓
              Redis
                 ↓
        Go WebSocket Service
```

---

## 📁 Estrutura

```bash
taskflow-pro/
├── backend/
├── frontend/
├── realtime-service/
├── docker-compose.yml
└── README.md
```

---

## 🐳 Rodando o projeto

```bash
git clone https://github.com/fprobstv/taskflow.git

cd taskflow

docker compose up -d
```

---

## Rodando o backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # No Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
``` 

---

## 🎯 Objetivo

Projeto criado para praticar:

- microsserviços
- sistemas distribuídos
- WebSockets
- Docker
- comunicação em tempo real

---

## 👨‍💻 Autor

Felipe Probst