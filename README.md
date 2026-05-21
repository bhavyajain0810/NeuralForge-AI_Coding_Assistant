# ⚡ Neural Forge — AI Coding Assistant

> A full-stack, AI-powered developer cockpit for debugging, explaining, optimizing, and documenting code

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docker.com)
[![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-yellow)](https://aistudio.google.com)
[![Live Demo](https://img.shields.io/badge/Live-Demo-Streamlit-FF4B4B?logo=streamlit)](https://neuralforge-aicodingassistant-7ukfwnccth79mgreuwa9sd.streamlit.app/)
[![API](https://img.shields.io/badge/API-Render-46E3B7)](https://neuralforge-ai-coding-assistant.onrender.com/docs)


---

## 🎯 Why this project

| Function | How this project demonstrates it |
|---|---|
| Scalable applications & services | FastAPI REST API with 11+ endpoints, Pydantic validation, health checks |
| Clean, maintainable code | Modular backend/frontend, structured prompts, logging |
| AI/LLM prototypes & tooling | Gemini integration for real dev workflows (debug, refactor, docs) |
| AI-assisted development | Uses Cursor/Copilot-style workflows; built with AI pair programming |
| Cloud & containerization | Docker Compose locally; **Streamlit Cloud** + **Render** in production |
| Experimentation mindset | Multiple AI features: chat, repo scan, complexity, commits |

---

## ✨ Features

| Module | Endpoint | What it does |
|---|---|---|
| 🔍 Explain | `POST /explain` | Plain-English code walkthrough |
| 🐛 Debug | `POST /debug` | Bug detection + fixed code |
| ⚡ Optimize | `POST /optimize` | Performance & best practices |
| 🔧 Refactor | `POST /refactor` | Structured refactoring |
| 💬 Ask AI | `POST /chat` | Free-form Q&A about your code |
| 📄 README | `POST /generate-readme` | Auto `README.md` |
| 📝 Commits | `POST /commit-message` | Conventional Commits from diff |
| 📊 Big-O | `POST /complexity` | Time/space complexity |
| 🗂️ Repo Scan | `POST /repo-summary` | Multi-file architecture analysis |
| 📁 Upload | `POST /upload-snippet` | Analyze uploaded source files |

**UI:** Cyberpunk “Neural Forge” cockpit — animated particle mesh, glass panels, terminal output, session history.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│          Streamlit Community Cloud (Production UI)               │
│   neuralforge-aicodingassistant-*.streamlit.app                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON  (BACKEND_URL secret)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Render — FastAPI Backend (Production API)           │
│   neuralforge-ai-coding-assistant.onrender.com · /docs · /health │
│         Pydantic · CORS · Swagger · Logging · Health checks        │
└────────────────────────────┬────────────────────────────────────┘
                             │ google-generativeai SDK
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Google Gemini 1.5 Flash (LLM API)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Gemini API Key](https://aistudio.google.com/app/apikey) (free tier)
- Docker (optional)

### 1. Clone & configure

```bash
git clone https://github.com/bhavyajain0810/NeuralForge-AI_Coding_Assistant.git
cd NeuralForge-AI_Coding_Assistant
cp backend/.env.example backend/.env
# Edit backend/.env → paste GEMINI_API_KEY
```

### 2. Run with Docker (recommended)

```bash
docker-compose up --build
```

- **UI:** http://localhost:8501
- **API:** http://localhost:8000
- **Swagger:** http://localhost:8000/docs

### 3. Local development

```bash
# Terminal 1 — Backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
NeuralForge-AI_Coding_Assistant/
├── backend/
│   ├── main.py              # FastAPI — all REST endpoints
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app.py               # Neural Forge Streamlit UI
│   ├── styles.py            # Cyberpunk CSS + particles
│   └── requirements.txt
├── streamlit_app.py         # Streamlit Cloud entry point
├── requirements.txt         # Root deps for Streamlit Cloud
├── render.yaml              # Render Blueprint config
├── DEPLOY.md                # Deployment guide
├── Dockerfile               # Multi-stage (backend + frontend)
├── docker-compose.yml       # Health checks + networking
├── .gitignore
└── README.md
```

---

## 🔌 API Examples

### Production (Render)

```bash
# Health check
curl https://neuralforge-ai-coding-assistant.onrender.com/health

# Explain code
curl -X POST https://neuralforge-ai-coding-assistant.onrender.com/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a,b): return a+b", "task": "Explain", "language": "Python"}'
```

Interactive docs: **[https://neuralforge-ai-coding-assistant.onrender.com/docs](https://neuralforge-ai-coding-assistant.onrender.com/docs)**

### Local

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"code": "x = [1,2,3]", "question": "What is the time complexity of copying this list?"}'
```

Local Swagger: **http://localhost:8000/docs**

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Frontend | Streamlit, custom CSS, HTML5 canvas particles |
| AI | Google Gemini 1.5 Flash (`google-generativeai`) |
| DevOps | Docker, Docker Compose, health checks |
| Deployment | [Streamlit Community Cloud](https://streamlit.io/cloud) (UI), [Render](https://render.com) (API) |
| API style | REST, OpenAPI/Swagger, multipart upload |

---

## 🌐 Deploy

| Service | Platform | URL / config |
|---|---|---|
| **Frontend** | [Streamlit Community Cloud](https://streamlit.io/cloud) | [Live app](https://neuralforge-aicodingassistant-7ukfwnccth79mgreuwa9sd.streamlit.app/) · Main file: `streamlit_app.py` · Secret: `BACKEND_URL` |
| **Backend** | [Render](https://render.com) | [API](https://neuralforge-ai-coding-assistant.onrender.com) · Env: `GEMINI_API_KEY` |

Full step-by-step instructions: **[DEPLOY.md](DEPLOY.md)**

---

## 🔗 Live Demo

| | Link |
|--|------|
| **App (UI)** | [neuralforge-aicodingassistant.streamlit.app](https://neuralforge-aicodingassistant-7ukfwnccth79mgreuwa9sd.streamlit.app/) |
| **API** | [neuralforge-ai-coding-assistant.onrender.com](https://neuralforge-ai-coding-assistant.onrender.com) |
| **Swagger** | [/docs](https://neuralforge-ai-coding-assistant.onrender.com/docs) |
| **Health** | [/health](https://neuralforge-ai-coding-assistant.onrender.com/health) |
| **GitHub** | [NeuralForge-AI_Coding_Assistant](https://github.com/bhavyajain0810/NeuralForge-AI_Coding_Assistant) |
