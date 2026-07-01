"""Neural Forge Streamlit frontend."""

from __future__ import annotations

import os
import time
from typing import Any

import streamlit as st

from api_client import APIClientError, NeuralForgeClient
from styles import FEATURE_GRID_HTML, GLOBAL_CSS, HERO_HTML

MAX_CODE_CHARS = 50_000
MAX_DIFF_CHARS = 30_000
MAX_UPLOAD_BYTES = 200_000

FEATURES = {
    "home": "⚡ Command Center",
    "explain": "🔍 Explain Code",
    "debug": "🐛 Debug Code",
    "optimize": "🚀 Optimize",
    "refactor": "🛠️ Refactor",
    "chat": "💬 Ask AI",
    "readme": "📄 README",
    "commit": "📝 Commits",
    "complexity": "📊 Big-O",
    "repo": "🗂️ Repo Scan",
    "upload": "📁 Upload",
}

LANGUAGES = [
    "auto-detect",
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "Go",
    "C++",
    "C",
    "Rust",
    "SQL",
    "Shell",
    "Scala",
]

SAMPLES = {
    "Python — recursive Fibonacci": """def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))""",
    "JavaScript — async bug": """async function fetchUser(id) {
  const response = fetch(`https://api.example.com/users/${id}`);
  return response.json();
}""",
    "Python — refactoring candidate": """def p(data):
    result = []
    for key, value in data.items():
        if value > 0:
            result.append(key)
    return result""",
}

CODE_TASKS = {
    "explain": {
        "title": "Explain code",
        "description": "Get a plain-language walkthrough, key concepts, and an example use case.",
        "button": "Explain code",
        "endpoint": "/explain",
        "history": "Explain",
    },
    "debug": {
        "title": "Debug code",
        "description": "Identify likely defects, understand root causes, and get a corrected version.",
        "button": "Find and fix issues",
        "endpoint": "/debug",
        "history": "Debug",
    },
    "optimize": {
        "title": "Optimize code",
        "description": "Review performance, memory use, maintainability, and relevant trade-offs.",
        "button": "Optimize code",
        "endpoint": "/optimize",
        "history": "Optimize",
    },
}


def get_backend_url() -> str:
    """Resolve the API URL from the environment without displaying its value."""
    return os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")


st.set_page_config(
    page_title="Neural Forge | AI Coding Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

BACKEND_URL = get_backend_url()
client = NeuralForgeClient(BACKEND_URL)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "responses" not in st.session_state:
    st.session_state.responses = {}


@st.cache_data(ttl=20, show_spinner=False)
def backend_status(base_url: str) -> tuple[bool, dict[str, Any]]:
    """Return backend reachability and health details."""
    try:
        return True, NeuralForgeClient(base_url).health()
    except APIClientError:
        return False, {}


def page_heading(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="nf-page-heading">
          <div class="nf-page-kicker">Neural module // developer workspace</div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_sample(prefix: str) -> None:
    sample_name = st.session_state.get(f"{prefix}_sample")
    if sample_name in SAMPLES:
        st.session_state[f"{prefix}_code"] = SAMPLES[sample_name]


def code_workspace(prefix: str, height: int = 285) -> tuple[str, str]:
    """Render a consistent code editor and its controls."""
    code_key = f"{prefix}_code"
    if code_key not in st.session_state:
        st.session_state[code_key] = ""

    language_column, sample_column = st.columns([1, 2])
    with language_column:
        language = st.selectbox("Language", LANGUAGES, key=f"{prefix}_language")
    with sample_column:
        st.selectbox(
            "Load an example",
            ["Choose an example…", *SAMPLES],
            key=f"{prefix}_sample",
            on_change=load_sample,
            args=(prefix,),
        )

    code = st.text_area(
        "Source code",
        key=code_key,
        height=height,
        placeholder=(
            "Paste the code you want Neural Forge to review. "
            "Include enough surrounding context for a useful answer."
        ),
        help=f"Maximum {MAX_CODE_CHARS:,} characters.",
    )
    st.caption(f"{len(code):,} / {MAX_CODE_CHARS:,} characters")
    return code, language


def validate_text(
    value: str,
    label: str,
    max_chars: int = MAX_CODE_CHARS,
) -> bool:
    cleaned = value.strip()
    if not cleaned:
        st.warning(f"Add {label} before submitting.")
        return False
    if len(cleaned) > max_chars:
        st.warning(
            f"{label.capitalize()} is too long "
            f"({len(cleaned):,} characters). The limit is {max_chars:,}."
        )
        return False
    return True


def show_api_error(error: APIClientError) -> None:
    if error.kind == "unreachable":
        st.error("Backend unavailable", icon="🔌")
        st.caption(
            f"{error.message} For local development, run "
            "`uvicorn backend.main:app --reload` from the repository root."
        )
    elif error.kind == "configuration":
        st.error("AI service is not configured", icon="🔑")
        st.caption(
            f"{error.message} Set `GEMINI_API_KEY` in `backend/.env` locally "
            "or in the backend host's environment."
        )
    elif error.kind == "timeout":
        st.error("The AI request took too long", icon="⏱️")
        st.caption(error.message)
    elif error.kind == "provider":
        st.error("Gemini could not complete the request", icon="🛰️")
        st.caption(error.message)
    else:
        st.error("The request could not be completed", icon="⚠️")
        st.caption(error.message)


def add_history(feature: str, input_chars: int, elapsed: float) -> None:
    st.session_state.history.insert(
        0,
        {
            "feature": feature,
            "chars": input_chars,
            "elapsed": elapsed,
            "time": time.strftime("%H:%M"),
        },
    )
    st.session_state.history = st.session_state.history[:8]


def save_response(
    key: str,
    title: str,
    text: str,
    elapsed: float,
    input_chars: int,
) -> None:
    st.session_state.responses[key] = {
        "title": title,
        "text": text,
        "elapsed": elapsed,
        "input_chars": input_chars,
    }


def run_analysis(
    key: str,
    endpoint: str,
    payload: dict[str, Any],
    title: str,
    input_chars: int,
) -> str | None:
    started_at = time.perf_counter()
    try:
        with st.spinner("Generating a structured response…"):
            result = client.analyze(endpoint, payload)
    except APIClientError as error:
        show_api_error(error)
        return None

    elapsed = round(time.perf_counter() - started_at, 2)
    save_response(key, title, result, elapsed, input_chars)
    add_history(title, input_chars, elapsed)
    return result


def run_upload(
    key: str,
    filename: str,
    content: bytes,
    task: str,
    input_chars: int,
) -> str | None:
    started_at = time.perf_counter()
    try:
        with st.spinner("Uploading and analyzing the file…"):
            result = client.upload(filename, content, task)
    except APIClientError as error:
        show_api_error(error)
        return None

    elapsed = round(time.perf_counter() - started_at, 2)
    save_response(key, f"Analysis of {filename}", result, elapsed, input_chars)
    add_history(f"Upload: {filename}", input_chars, elapsed)
    return result


def render_response(key: str) -> None:
    response = st.session_state.responses.get(key)
    if not response:
        return

    st.divider()
    with st.container(border=True):
        st.markdown(
            '<div class="nf-response-title">'
            '<span class="nf-response-dot"></span>AI response</div>',
            unsafe_allow_html=True,
        )
        st.markdown(response["text"])
        st.caption(
            f"{response['title']} · {response['elapsed']:.2f}s · "
            f"{len(response['text']):,} output characters"
        )

        download_column, raw_column = st.columns([1, 2])
        with download_column:
            st.download_button(
                "Download as Markdown",
                response["text"],
                file_name=f"neural-forge-{key}.md",
                mime="text/markdown",
                key=f"{key}_download",
                use_container_width=True,
            )
        with raw_column:
            with st.expander("Copy-friendly raw output"):
                st.code(response["text"], language="markdown")


def render_standard_code_task(key: str) -> None:
    task = CODE_TASKS[key]
    page_heading(task["title"], task["description"])
    code, language = code_workspace(key)
    if st.button(
        task["button"],
        type="primary",
        use_container_width=True,
        key=f"{key}_submit",
    ):
        if validate_text(code, "source code"):
            run_analysis(
                key,
                task["endpoint"],
                {"code": code.strip(), "task": task["history"], "language": language},
                task["history"],
                len(code.strip()),
            )
    render_response(key)


online, health = backend_status(BACKEND_URL)
api_configured = bool(health.get("api_configured")) if online else False

with st.sidebar:
    st.markdown(
        """
        <div class="nf-side-brand">
          <div class="nf-side-logo"><span>⚡</span> NEURAL FORGE</div>
          <div class="nf-side-sub">AI developer command center</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if online and api_configured:
        st.markdown(
            '<span class="nf-status online">Backend ready</span>',
            unsafe_allow_html=True,
        )
    elif online:
        st.markdown(
            '<span class="nf-status degraded">API key needed</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="nf-status offline">Backend offline</span>',
            unsafe_allow_html=True,
        )

    if online:
        st.caption(f"Active model: `{health.get('model', 'Not reported')}`")
    else:
        st.caption("Start the API or check `BACKEND_URL`.")

    if st.button("Refresh status", use_container_width=True):
        backend_status.clear()
        st.rerun()

    st.markdown('<div class="nf-section-label">Developer modules</div>', unsafe_allow_html=True)
    labels = list(FEATURES.values())
    keys = list(FEATURES)
    selected_index = keys.index(st.session_state.page)
    selected_label = st.radio(
        "Choose a task",
        labels,
        index=selected_index,
    )
    st.session_state.page = keys[labels.index(selected_label)]

    st.divider()
    with st.expander("How to use Neural Forge", expanded=False):
        st.markdown(
            "1. Choose a task.\n"
            "2. Select a language or use auto-detect.\n"
            "3. Paste focused code and relevant context.\n"
            "4. Review the answer before applying changes."
        )

    st.markdown("**Runtime & settings**")
    st.caption("FastAPI · Streamlit · Gemini · Docker")
    st.caption(f"Input limit: `{MAX_CODE_CHARS:,} chars` · Timeout: `{client.timeout}s`")
    st.link_button("Open API documentation", f"{BACKEND_URL}/docs", use_container_width=True)

    if st.session_state.history:
        st.divider()
        st.markdown("**Recent activity**")
        for item in st.session_state.history[:5]:
            st.caption(
                f"`{item['time']}` {item['feature']} · "
                f"{item['chars']:,} chars · {item['elapsed']:.1f}s"
            )


page = st.session_state.page

if page == "home":
    st.markdown(HERO_HTML, unsafe_allow_html=True)
    st.markdown(
        '<div class="nf-section-label">Developer tool matrix</div>',
        unsafe_allow_html=True,
    )
    st.markdown(FEATURE_GRID_HTML, unsafe_allow_html=True)

    status_label = (
        "Ready"
        if online and api_configured
        else "Key needed"
        if online
        else "Offline"
    )
    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("API status", status_label)
    metric_2.metric("Active model", health.get("model", "—") if online else "—")
    metric_3.metric("REST endpoints", "11")
    metric_4.metric("Session runs", len(st.session_state.history))

    st.markdown(
        '<div class="nf-section-label">Engineering dashboard</div>',
        unsafe_allow_html=True,
    )
    architecture_column, workflow_column, delivery_column = st.columns(3)
    with architecture_column:
        with st.container(border=True):
            st.markdown("#### API engineering")
            st.markdown(
                "Typed request validation, response contracts, health reporting, "
                "file limits, and documented REST endpoints."
            )
    with workflow_column:
        with st.container(border=True):
            st.markdown("#### AI workflows")
            st.markdown(
                "Gemini-backed explanation, debugging, optimization, refactoring, "
                "documentation, and repository analysis."
            )
    with delivery_column:
        with st.container(border=True):
            st.markdown("#### Delivery ready")
            st.markdown(
                "Separate frontend and backend services, Docker Compose orchestration, "
                "deployment manifests, and runtime status visibility."
            )

    if not online:
        st.info(
            "The interface is available, but AI tasks need the backend. "
            "Run `uvicorn backend.main:app --reload` and refresh the status.",
            icon="ℹ️",
        )
    elif not api_configured:
        st.warning(
            "The backend is running without a Gemini API key. "
            "Add `GEMINI_API_KEY` to `backend/.env`, then restart the API.",
            icon="🔑",
        )

    with st.expander("Local developer launch commands"):
        st.code("uvicorn backend.main:app --reload", language="bash")
        st.code("streamlit run streamlit_app.py", language="bash")

    if st.session_state.responses:
        latest_key = next(reversed(st.session_state.responses))
        st.markdown(
            '<div class="nf-section-label">Latest neural output</div>',
            unsafe_allow_html=True,
        )
        render_response(latest_key)

elif page in CODE_TASKS:
    render_standard_code_task(page)

elif page == "refactor":
    page_heading(
        "Refactor code",
        "Improve structure and maintainability around a goal you define.",
    )
    refactor_code, refactor_language = code_workspace("refactor")
    refactor_goal = st.text_input(
        "Refactoring goal",
        value="Improve readability, naming, and maintainability",
        max_chars=300,
    )
    if st.button(
        "Refactor code",
        type="primary",
        use_container_width=True,
        key="refactor_submit",
    ):
        if validate_text(refactor_code, "source code") and validate_text(
            refactor_goal, "refactoring goal", 300
        ):
            run_analysis(
                "refactor",
                "/refactor",
                {
                    "code": refactor_code.strip(),
                    "goal": refactor_goal.strip(),
                    "language": refactor_language,
                },
                "Refactor",
                len(refactor_code.strip()),
            )
    render_response("refactor")

elif page == "chat":
    page_heading(
        "Ask about code",
        "Use Neural Forge as a pair programmer for design, edge cases, or implementation questions.",
    )
    chat_code, chat_language = code_workspace("chat", height=245)
    question = st.text_area(
        "Question",
        height=110,
        placeholder="For example: Why does this fail on empty input, and how should I test the fix?",
        max_chars=2_000,
    )
    if st.button(
        "Ask Neural Forge",
        type="primary",
        use_container_width=True,
        key="chat_submit",
    ):
        if validate_text(chat_code, "source code") and validate_text(
            question, "a question", 2_000
        ):
            run_analysis(
                "chat",
                "/chat",
                {
                    "code": chat_code.strip(),
                    "question": question.strip(),
                    "language": chat_language,
                },
                "Pair programming",
                len(chat_code.strip()),
            )
    render_response("chat")

elif page == "readme":
    page_heading(
        "Generate a README",
        "Turn project context, source code, or setup notes into structured documentation.",
    )
    project_context = st.text_area(
        "Project context",
        height=300,
        placeholder=(
            "Describe the project and paste important files or setup details. "
            "Include the target audience, commands, and key features when known."
        ),
        help=f"Maximum {MAX_CODE_CHARS:,} characters.",
    )
    st.caption(f"{len(project_context):,} / {MAX_CODE_CHARS:,} characters")
    if st.button(
        "Generate README",
        type="primary",
        use_container_width=True,
        key="readme_submit",
    ):
        if validate_text(project_context, "project context"):
            run_analysis(
                "readme",
                "/generate-readme",
                {
                    "code": project_context.strip(),
                    "task": "README",
                    "language": "auto-detect",
                },
                "README",
                len(project_context.strip()),
            )
    render_response("readme")

elif page == "commit":
    page_heading(
        "Generate commit messages",
        "Create ranked Conventional Commit options from a focused git diff.",
    )
    git_diff = st.text_area(
        "Git diff",
        height=290,
        placeholder="Paste the output of `git diff` here.",
        help=f"Maximum {MAX_DIFF_CHARS:,} characters.",
    )
    st.caption(f"{len(git_diff):,} / {MAX_DIFF_CHARS:,} characters")
    if st.button(
        "Generate commit messages",
        type="primary",
        use_container_width=True,
        key="commit_submit",
    ):
        if validate_text(git_diff, "a git diff", MAX_DIFF_CHARS):
            run_analysis(
                "commit",
                "/commit-message",
                {"diff": git_diff.strip()},
                "Commit messages",
                len(git_diff.strip()),
            )
    render_response("commit")

elif page == "complexity":
    page_heading(
        "Analyze complexity",
        "Estimate time and space complexity, identify bottlenecks, and compare improvements.",
    )
    complexity_code, complexity_language = code_workspace("complexity")
    if st.button(
        "Analyze complexity",
        type="primary",
        use_container_width=True,
        key="complexity_submit",
    ):
        if validate_text(complexity_code, "source code"):
            run_analysis(
                "complexity",
                "/complexity",
                {
                    "code": complexity_code.strip(),
                    "language": complexity_language,
                },
                "Complexity analysis",
                len(complexity_code.strip()),
            )
    render_response("complexity")

elif page == "repo":
    page_heading(
        "Summarize a repository",
        "Review up to five representative files for architecture, data flow, and improvements.",
    )
    repository_files: dict[str, str] = {}
    incomplete_files = False
    tabs = st.tabs([f"File {index}" for index in range(1, 6)])
    for index, tab in enumerate(tabs, start=1):
        with tab:
            filename = st.text_input(
                "File path",
                key=f"repo_filename_{index}",
                placeholder="backend/main.py",
                max_chars=200,
            )
            content = st.text_area(
                "File content",
                key=f"repo_content_{index}",
                height=145,
                placeholder="Paste this file's content.",
            )
            if bool(filename.strip()) != bool(content.strip()):
                incomplete_files = True
            if filename.strip() and content.strip():
                repository_files[filename.strip()] = content.strip()

    total_repository_chars = sum(len(content) for content in repository_files.values())
    st.caption(
        f"{len(repository_files)} files selected · "
        f"{total_repository_chars:,} / {MAX_CODE_CHARS:,} total characters"
    )
    if st.button(
        "Summarize repository",
        type="primary",
        use_container_width=True,
        key="repo_submit",
    ):
        if incomplete_files:
            st.warning("Each included file needs both a path and content.")
        elif not repository_files:
            st.warning("Add at least one file before submitting.")
        elif total_repository_chars > MAX_CODE_CHARS:
            st.warning(
                f"The combined file content exceeds the {MAX_CODE_CHARS:,}-character limit."
            )
        else:
            run_analysis(
                "repo",
                "/repo-summary",
                {"files": repository_files},
                "Repository summary",
                total_repository_chars,
            )
    render_response("repo")

elif page == "upload":
    page_heading(
        "Upload a source file",
        "Analyze one text-based source file without pasting it into the editor.",
    )
    upload_task = st.selectbox(
        "Analysis mode",
        [
            "Explain this code",
            "Debug this code",
            "Optimize this code",
            "Analyze complexity",
        ],
    )
    uploaded_file = st.file_uploader(
        "Source file",
        type=["py", "js", "ts", "java", "go", "cpp", "c", "rs", "txt", "md", "sql"],
        help="Text files only; maximum 200 KB.",
    )
    upload_content = b""
    upload_preview = ""
    if uploaded_file is not None:
        upload_content = uploaded_file.getvalue()
        upload_preview = upload_content.decode("utf-8", errors="replace")
        st.caption(f"{uploaded_file.name} · {len(upload_content):,} bytes")
        with st.expander("File preview", expanded=True):
            st.code(
                upload_preview[:8_000],
                language=(
                    uploaded_file.name.rsplit(".", 1)[-1]
                    if "." in uploaded_file.name
                    else "text"
                ),
            )

    if st.button(
        "Analyze file",
        type="primary",
        use_container_width=True,
        key="upload_submit",
        disabled=uploaded_file is None,
    ):
        if not upload_content:
            st.warning("Choose a non-empty source file.")
        elif len(upload_content) > MAX_UPLOAD_BYTES:
            st.warning(
                f"The selected file is too large ({len(upload_content):,} bytes). "
                f"The limit is {MAX_UPLOAD_BYTES:,} bytes."
            )
        elif len(upload_preview) > MAX_CODE_CHARS:
            st.warning(
                f"The decoded file exceeds the {MAX_CODE_CHARS:,}-character analysis limit."
            )
        else:
            run_upload(
                "upload",
                uploaded_file.name,
                upload_content,
                upload_task,
                len(upload_preview),
            )
    render_response("upload")

st.markdown(
    """
    <div class="nf-footer">
      NEURAL FORGE // FastAPI + Streamlit + Google Gemini + Docker // AI DEVELOPER COCKPIT
    </div>
    """,
    unsafe_allow_html=True,
)
