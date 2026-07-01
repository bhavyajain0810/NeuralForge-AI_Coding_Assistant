"""FastAPI service for Neural Forge."""

from __future__ import annotations

import logging
import os
from pathlib import Path
import time
from typing import Annotated, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from pydantic import BaseModel, ConfigDict, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger("neural_forge")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

APP_VERSION = "3.0.0"
MAX_CODE_CHARS = 50_000
MAX_DIFF_CHARS = 30_000
MAX_REPO_FILES = 10
MAX_FILE_CHARS = 20_000
MAX_UPLOAD_BYTES = 200_000
MAX_OUTPUT_TOKENS = 4_096

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
] or ["*"]

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(MODEL_NAME)
else:
    gemini_model = None

if not GEMINI_API_KEY:
    logger.warning(
        "GEMINI_API_KEY is not configured; health checks will report degraded status."
    )


app = FastAPI(
    title="Neural Forge AI Coding Assistant API",
    description=(
        "Validated REST API for AI-assisted code analysis, debugging, "
        "optimization, documentation, and developer workflows."
    ),
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class StrictRequest(BaseModel):
    """Base request that strips whitespace and rejects unknown fields."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class CodeRequest(StrictRequest):
    code: str = Field(min_length=1, max_length=MAX_CODE_CHARS)
    task: str = Field(default="Analyze", min_length=1, max_length=100)
    language: str = Field(default="auto-detect", min_length=1, max_length=50)


class CommitRequest(StrictRequest):
    diff: str = Field(min_length=1, max_length=MAX_DIFF_CHARS)


class ComplexityRequest(StrictRequest):
    code: str = Field(min_length=1, max_length=MAX_CODE_CHARS)
    language: str = Field(default="auto-detect", min_length=1, max_length=50)


class RepoSummaryRequest(StrictRequest):
    files: dict[str, str] = Field(min_length=1, max_length=MAX_REPO_FILES)

    @field_validator("files")
    @classmethod
    def validate_files(cls, files: dict[str, str]) -> dict[str, str]:
        cleaned_files: dict[str, str] = {}
        total_chars = 0

        for raw_name, raw_content in files.items():
            name = raw_name.strip()
            content = raw_content.strip()
            if not name:
                raise ValueError("Every repository file needs a path.")
            if len(name) > 200:
                raise ValueError(f"File path is too long: {name[:40]}…")
            if not content:
                raise ValueError(f"File '{name}' has no content.")
            if len(content) > MAX_FILE_CHARS:
                raise ValueError(
                    f"File '{name}' exceeds the {MAX_FILE_CHARS:,}-character limit."
                )
            if name in cleaned_files:
                raise ValueError(f"Duplicate file path: '{name}'.")

            cleaned_files[name] = content
            total_chars += len(content)

        if total_chars > MAX_CODE_CHARS:
            raise ValueError(
                f"Combined repository content exceeds {MAX_CODE_CHARS:,} characters."
            )
        return cleaned_files


class ChatRequest(StrictRequest):
    code: str = Field(min_length=1, max_length=MAX_CODE_CHARS)
    question: str = Field(min_length=1, max_length=2_000)
    language: str = Field(default="auto-detect", min_length=1, max_length=50)


class RefactorRequest(StrictRequest):
    code: str = Field(min_length=1, max_length=MAX_CODE_CHARS)
    goal: str = Field(
        default="Improve readability and maintainability",
        min_length=1,
        max_length=300,
    )
    language: str = Field(default="auto-detect", min_length=1, max_length=50)


class AIResponse(BaseModel):
    response: str


class AnalyzeResponse(AIResponse):
    task: str
    language: str


class RootResponse(BaseModel):
    status: Literal["ok"]
    message: str
    docs: str
    health: str


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    model: str
    api_configured: bool
    version: str


class EndpointInfo(BaseModel):
    method: Literal["POST"]
    path: str
    description: str


class APIInfoResponse(BaseModel):
    name: str
    endpoints: list[EndpointInfo]


def call_llm(prompt: str) -> str:
    """Send a prompt to Gemini and map provider failures to safe API errors."""
    if gemini_model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Gemini API is not configured. Set GEMINI_API_KEY in the "
                "backend environment and restart the service."
            ),
        )

    started_at = time.perf_counter()
    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config={"max_output_tokens": MAX_OUTPUT_TOKENS},
        )
        text = response.text
        if not text or not text.strip():
            raise ValueError("Gemini returned no text.")
    except (
        google_exceptions.Unauthenticated,
        google_exceptions.PermissionDenied,
    ) as error:
        logger.warning("Gemini authentication or permission check failed.")
        raise HTTPException(
            status_code=502,
            detail="Gemini authentication failed. Verify the server API key.",
        ) from error
    except google_exceptions.ResourceExhausted as error:
        logger.warning("Gemini rate limit or quota was reached.")
        raise HTTPException(
            status_code=503,
            detail="Gemini rate limit reached. Wait briefly and try again.",
        ) from error
    except google_exceptions.NotFound as error:
        logger.warning("The configured Gemini model was not found.")
        raise HTTPException(
            status_code=502,
            detail="The configured Gemini model is unavailable.",
        ) from error
    except google_exceptions.InvalidArgument as error:
        logger.warning("Gemini rejected an invalid request.")
        raise HTTPException(
            status_code=400,
            detail="Gemini rejected the request. Try a smaller or simpler input.",
        ) from error
    except google_exceptions.GoogleAPIError as error:
        logger.warning(
            "Gemini request failed with provider error type %s.",
            type(error).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="Gemini could not complete the request. Try again shortly.",
        ) from error
    except ValueError as error:
        logger.warning("Gemini returned an empty or blocked response.")
        raise HTTPException(
            status_code=502,
            detail=(
                "Gemini returned no usable text. Revise the input and try again."
            ),
        ) from error
    except Exception as error:
        logger.exception(
            "Unexpected Gemini client failure (%s).", type(error).__name__
        )
        raise HTTPException(
            status_code=502,
            detail="The AI provider is temporarily unavailable.",
        ) from error

    elapsed = time.perf_counter() - started_at
    logger.info("Gemini request completed in %.2fs.", elapsed)
    return text.strip()


@app.get("/", response_model=RootResponse, tags=["Health"])
def root() -> RootResponse:
    return RootResponse(
        status="ok",
        message="Neural Forge AI Coding Assistant API",
        docs="/docs",
        health="/health",
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy" if GEMINI_API_KEY else "degraded",
        model=MODEL_NAME,
        api_configured=bool(GEMINI_API_KEY),
        version=APP_VERSION,
    )


@app.get("/api-info", response_model=APIInfoResponse, tags=["Health"])
def api_info() -> APIInfoResponse:
    endpoints = [
        EndpointInfo(method="POST", path="/analyze", description="General code analysis"),
        EndpointInfo(method="POST", path="/explain", description="Plain-English explanation"),
        EndpointInfo(method="POST", path="/debug", description="Bug detection and fixes"),
        EndpointInfo(method="POST", path="/optimize", description="Performance optimization"),
        EndpointInfo(method="POST", path="/refactor", description="Structured refactoring"),
        EndpointInfo(
            method="POST",
            path="/generate-readme",
            description="README generation",
        ),
        EndpointInfo(
            method="POST",
            path="/commit-message",
            description="Conventional commit messages",
        ),
        EndpointInfo(method="POST", path="/complexity", description="Big-O analysis"),
        EndpointInfo(
            method="POST",
            path="/repo-summary",
            description="Multi-file architecture summary",
        ),
        EndpointInfo(method="POST", path="/chat", description="Questions about code"),
        EndpointInfo(
            method="POST",
            path="/upload-snippet",
            description="Source file upload",
        ),
    ]
    return APIInfoResponse(name="Neural Forge API", endpoints=endpoints)


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Core"])
def analyze_code(request: CodeRequest) -> AnalyzeResponse:
    prompt = f"""
You are a senior software engineer. Language: {request.language}.
Task: {request.task}

Code:
```
{request.code}
```

Be concise, structured, and actionable. Use Markdown formatting.
"""
    return AnalyzeResponse(
        task=request.task,
        language=request.language,
        response=call_llm(prompt),
    )


@app.post("/explain", response_model=AIResponse, tags=["Core"])
def explain_code(request: CodeRequest) -> AIResponse:
    prompt = f"""
You are a coding instructor. Language: {request.language}.

Explain this code clearly:
```
{request.code}
```

Cover: Overview, Step-by-Step Breakdown, Key Concepts, and an Example Use Case.
Use Markdown and fenced code blocks where helpful.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/debug", response_model=AIResponse, tags=["Core"])
def debug_code(request: CodeRequest) -> AIResponse:
    prompt = f"""
You are an expert debugger. Language: {request.language}.

Analyze this code for defects:
```
{request.code}
```

Return: Bugs Found, Root Cause, Fixed Code, and Prevention Tips.
Use Markdown and put corrected code in a fenced code block.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/optimize", response_model=AIResponse, tags=["Core"])
def optimize_code(request: CodeRequest) -> AIResponse:
    prompt = f"""
You are a performance engineer. Language: {request.language}.

Optimize this code:
```
{request.code}
```

Return: Issues, Optimized Code, Explanation, and Time/Space Complexity Before and After.
Use Markdown and put optimized code in a fenced code block.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/refactor", response_model=AIResponse, tags=["Core"])
def refactor_code(request: RefactorRequest) -> AIResponse:
    prompt = f"""
You are a refactoring specialist. Language: {request.language}.
Goal: {request.goal}

Refactor this code:
```
{request.code}
```

Return: Refactoring Plan, Refactored Code, What Changed, and Trade-offs.
Use Markdown and put refactored code in a fenced code block.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/chat", response_model=AIResponse, tags=["Core"])
def chat_about_code(request: ChatRequest) -> AIResponse:
    prompt = f"""
You are an AI pair programmer. Language: {request.language}.

Code:
```
{request.code}
```

Developer question: {request.question}

Answer clearly and reference specific parts of the code when relevant. Use Markdown.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/generate-readme", response_model=AIResponse, tags=["Documentation"])
def generate_readme(request: CodeRequest) -> AIResponse:
    prompt = f"""
You are a technical writer. Generate a complete professional README.md from:

```
{request.code}
```

Include when applicable: Title, Overview, Features, Tech Stack, Prerequisites,
Installation, Usage, API Reference, Project Structure, Contributing, and License.
Do not invent live URLs or commands not supported by the supplied context.
Return Markdown only.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/commit-message", response_model=AIResponse, tags=["Documentation"])
def generate_commit_message(request: CommitRequest) -> AIResponse:
    prompt = f"""
You are a Git expert. Generate commit messages for this diff:

```
{request.diff}
```

Use Conventional Commits (feat, fix, docs, refactor, perf, test, chore).
Return three options ranked from most descriptive to most concise. Use Markdown.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/complexity", response_model=AIResponse, tags=["Analysis"])
def analyze_complexity(request: ComplexityRequest) -> AIResponse:
    prompt = f"""
You are a computer science instructor. Language: {request.language}.

Analyze this code:
```
{request.code}
```

Return: Time Complexity, Space Complexity, Best/Average/Worst Case,
Bottlenecks, and Practical Optimizations. Use Markdown.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/repo-summary", response_model=AIResponse, tags=["Analysis"])
def repo_summary(request: RepoSummaryRequest) -> AIResponse:
    files_text = "\n\n".join(
        f"### {filename}\n```\n{content}\n```"
        for filename, content in request.files.items()
    )
    prompt = f"""
You are a software architect. Analyze this codebase:

{files_text}

Return: Project Overview, Architecture Summary, Data Flow, Key Components,
Detected Tech Stack, Risks, and Prioritized Improvements. Use Markdown.
"""
    return AIResponse(response=call_llm(prompt))


@app.post("/upload-snippet", response_model=AnalyzeResponse, tags=["Core"])
async def upload_snippet(
    file: Annotated[UploadFile, File(description="UTF-8 source file")],
    task: Annotated[
        str,
        Query(min_length=1, max_length=100),
    ] = "Explain this code",
) -> AnalyzeResponse:
    allowed_extensions = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".go",
        ".cpp",
        ".c",
        ".rs",
        ".txt",
        ".md",
        ".sql",
    }
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension or 'none'}'.",
        )

    content_bytes = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if len(content_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File is too large. Maximum size is {MAX_UPLOAD_BYTES:,} bytes.",
        )

    try:
        code = content_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise HTTPException(
            status_code=400,
            detail="File must contain UTF-8 text.",
        ) from error

    code = code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(code) > MAX_CODE_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Decoded file exceeds {MAX_CODE_CHARS:,} characters.",
        )

    request = CodeRequest(
        code=code,
        task=task,
        language=extension.lstrip(".") or "auto-detect",
    )
    return analyze_code(request)
