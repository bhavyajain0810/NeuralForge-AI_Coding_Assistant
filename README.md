# ⚡ Neural Forge — AI Coding Assistant

> A full-stack, AI-powered developer cockpit for debugging, explaining, optimizing, and documenting code — built for **Software Engineering Intern** roles at AI-forward companies like **Demandbase**.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docker.com)
[![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-yellow)](https://aistudio.google.com)

---

## 🎯 Why this project

| Function | How this project demonstrates it |
|---|---|
| Scalable applications & services | FastAPI REST API with 11+ endpoints, Pydantic validation, health checks |
| Clean, maintainable code | Modular backend/frontend, structured prompts, logging |
| AI/LLM prototypes & tooling | Gemini integration for real dev workflows (debug, refactor, docs) |
| AI-assisted development | Uses Cursor/Copilot-style workflows; built with AI pair programming |
| Cloud & containerization | Docker multi-stage build + Compose orchestration |
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
│                     Browser (Streamlit UI)                       │
│              Neural Forge · Port 8501 · Particle UI              │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend · Port 8000                    │
│         Pydantic models · CORS · Swagger /docs · Logging         │
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
git clone https://github.com/YOUR_USERNAME/ai-coding-assistant.git
cd ai-coding-assistant
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
ai-coding-assistant/
├── backend/
│   ├── main.py              # FastAPI — all REST endpoints
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app.py               # Neural Forge Streamlit UI
│   ├── styles.py            # Cyberpunk CSS + particles
│   └── requirements.txt
├── Dockerfile               # Multi-stage (backend + frontend)
├── docker-compose.yml       # Health checks + networking
├── .gitignore
└── README.md
```

---

## 🔌 API Examples

```bash
# Health check
curl http://localhost:8000/health

# Explain code
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a,b): return a+b", "task": "Explain", "language": "Python"}'

# Chat about code
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"code": "x = [1,2,3]", "question": "What is the time complexity of copying this list?"}'
```

Interactive docs: **http://localhost:8000/docs**

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Frontend | Streamlit, custom CSS, HTML5 canvas particles |
| AI | Google Gemini 1.5 Flash (`google-generativeai`) |
| DevOps | Docker, Docker Compose, health checks |
| API style | REST, OpenAPI/Swagger, multipart upload |

---

## 📄 Resume bullet points

Use these on your resume / cover letter:

- Built a **full-stack AI coding assistant** with **FastAPI** REST APIs and **Streamlit** UI, integrating **Google Gemini** for code explanation, debugging, refactoring, and documentation generation.
- Designed **11+ production-style API endpoints** with Pydantic validation, CORS, structured logging, and **Swagger/OpenAPI** documentation.
- **Containerized** the application with **Docker Compose**, including health checks and multi-service orchestration.
- Implemented **multi-file repo analysis**, file upload, Big-O complexity analysis, and **Conventional Commit** message generation.

---

## 🌐 Deploy

| Service | Platform |
|---|---|
| Frontend | [Streamlit Community Cloud](https://streamlit.io/cloud) — set `BACKEND_URL` |
| Backend | [Render](https://render.com) or [Railway](https://railway.app) |

---

## 📈 Roadmap

- [ ] LangChain agent chains for multi-step reasoning
- [ ] ChromaDB semantic code search
- [ ] GitHub API — PR analysis & auto-review
- [ ] JWT auth + rate limiting

---

## 📄 License

MIT
