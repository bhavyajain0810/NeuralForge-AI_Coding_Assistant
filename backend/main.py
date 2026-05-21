from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import google.generativeai as genai
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not set — API calls will fail until configured.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
else:
    model = None

app = FastAPI(
    title="Neural Forge — AI Coding Assistant API",
    description=(
        "Production-style REST API for AI-assisted code analysis, debugging, "
        "documentation, and developer workflow automation."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request models ──────────────────────────────────────────────

class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    task: str = "Analyze"
    language: Optional[str] = "auto-detect"

class CommitRequest(BaseModel):
    diff: str = Field(..., min_length=1, max_length=30000)

class ComplexityRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    language: Optional[str] = "auto-detect"

class RepoSummaryRequest(BaseModel):
    files: dict[str, str] = Field(..., max_length=10)

class ChatRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    question: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = "auto-detect"

class RefactorRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    goal: str = "Improve readability and maintainability"
    language: Optional[str] = "auto-detect"

# ── LLM helper ──────────────────────────────────────────────────

def call_llm(prompt: str) -> str:
    if not model:
        raise HTTPException(
            status_code=503,
            detail="Gemini API not configured. Set GEMINI_API_KEY in backend/.env",
        )
    try:
        start = time.time()
        response = model.generate_content(prompt)
        elapsed = round(time.time() - start, 2)
        logger.info("LLM call completed in %ss", elapsed)
        return response.text
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


# ── Endpoints ───────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "message": "Neural Forge API — AI Coding Assistant",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy" if GEMINI_API_KEY else "degraded",
        "model": MODEL_NAME,
        "api_configured": bool(GEMINI_API_KEY),
        "version": "2.0.0",
    }


@app.get("/api-info", tags=["Health"])
def api_info():
    return {
        "name": "Neural Forge API",
        "endpoints": [
            {"method": "POST", "path": "/analyze", "description": "General code analysis"},
            {"method": "POST", "path": "/explain", "description": "Plain-English explanation"},
            {"method": "POST", "path": "/debug", "description": "Bug detection and fixes"},
            {"method": "POST", "path": "/optimize", "description": "Performance optimization"},
            {"method": "POST", "path": "/refactor", "description": "Structured refactoring"},
            {"method": "POST", "path": "/generate-readme", "description": "README.md generation"},
            {"method": "POST", "path": "/commit-message", "description": "Conventional commit messages"},
            {"method": "POST", "path": "/complexity", "description": "Big-O analysis"},
            {"method": "POST", "path": "/repo-summary", "description": "Multi-file architecture summary"},
            {"method": "POST", "path": "/chat", "description": "Ask anything about your code"},
            {"method": "POST", "path": "/upload-snippet", "description": "Upload source file"},
        ],
    }


@app.post("/analyze", tags=["Core"])
def analyze_code(request: CodeRequest):
    prompt = f"""
You are a senior software engineer. Language: {request.language}.
Task: {request.task}

Code:
```
{request.code}
```

Be concise, structured, and actionable. Use markdown formatting.
"""
    result = call_llm(prompt)
    return {"task": request.task, "language": request.language, "response": result}


@app.post("/explain", tags=["Core"])
def explain_code(request: CodeRequest):
    prompt = f"""
You are a coding instructor. Language: {request.language}.

Explain this code clearly:
```
{request.code}
```

Cover: Overview, Step-by-Step Breakdown, Key Concepts, Example use-case.
Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/debug", tags=["Core"])
def debug_code(request: CodeRequest):
    prompt = f"""
You are an expert debugger. Language: {request.language}.

Analyze for bugs:
```
{request.code}
```

Return: Bugs Found, Root Cause, Fixed Code (with comments), Prevention Tips.
Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/optimize", tags=["Core"])
def optimize_code(request: CodeRequest):
    prompt = f"""
You are a performance engineer. Language: {request.language}.

Optimize:
```
{request.code}
```

Return: Issues, Optimized Code, Explanation, Time/Space Complexity before & after.
Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/refactor", tags=["Core"])
def refactor_code(request: RefactorRequest):
    prompt = f"""
You are a refactoring specialist. Language: {request.language}.
Goal: {request.goal}

Refactor this code:
```
{request.code}
```

Return: Refactoring Plan, Refactored Code, What Changed, Trade-offs.
Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/chat", tags=["Core"])
def chat_about_code(request: ChatRequest):
    prompt = f"""
You are an AI pair programmer. Language: {request.language}.

Code:
```
{request.code}
```

Developer question: {request.question}

Answer clearly and reference specific parts of the code when relevant. Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/generate-readme", tags=["Documentation"])
def generate_readme(request: CodeRequest):
    prompt = f"""
You are a technical writer. Generate a complete professional README.md from:

```
{request.code}
```

Include: Title, Overview, Features, Tech Stack, Prerequisites, Installation, Usage,
API Reference (if applicable), Project Structure, Contributing, License.
Use markdown only.
"""
    return {"response": call_llm(prompt)}


@app.post("/commit-message", tags=["Documentation"])
def generate_commit_message(request: CommitRequest):
    prompt = f"""
You are a Git expert. Generate commit messages for this diff:

```
{request.diff}
```

Use Conventional Commits (feat, fix, docs, refactor, perf, test, chore).
Return 3 options ranked best to most concise. Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/complexity", tags=["Analysis"])
def analyze_complexity(request: ComplexityRequest):
    prompt = f"""
You are a CS professor. Language: {request.language}.

Analyze complexity:
```
{request.code}
```

Return: Time Complexity, Space Complexity, Worst/Average/Best Case, Bottlenecks, Optimizations.
Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/repo-summary", tags=["Analysis"])
def repo_summary(request: RepoSummaryRequest):
    if len(request.files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per request.")
    files_text = "\n\n".join(
        f"### {fname}\n```\n{content}\n```" for fname, content in request.files.items()
    )
    prompt = f"""
You are a software architect. Analyze this codebase:

{files_text}

Return: Project Overview, Architecture Summary, Data Flow, Key Components,
Tech Stack Detected, Suggested Improvements. Use markdown.
"""
    return {"response": call_llm(prompt)}


@app.post("/upload-snippet", tags=["Core"])
async def upload_snippet(file: UploadFile = File(...), task: str = "Explain this code"):
    allowed = {".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".rs", ".txt", ".md", ".sql"}
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"File type {ext} not supported.")

    content = await file.read()
    code = content.decode("utf-8", errors="ignore")
    if len(code) > 50000:
        raise HTTPException(status_code=400, detail="File too large. Max 50,000 characters.")

    request = CodeRequest(code=code, task=task, language=ext.lstrip(".") or "auto-detect")
    return analyze_code(request)
