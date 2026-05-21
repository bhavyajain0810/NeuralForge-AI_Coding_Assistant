"""
Neural Forge — AI Coding Assistant
A cinematic Streamlit cockpit wired to FastAPI + Gemini.
"""

import os
import time
import requests
import streamlit as st
import streamlit.components.v1 as components

from styles import GLOBAL_CSS, PARTICLE_HTML, HERO_HTML, FEATURE_GRID_HTML


def get_backend_url() -> str:
    """Streamlit Cloud secrets → env var → localhost."""
    try:
        if "BACKEND_URL" in st.secrets:
            return str(st.secrets["BACKEND_URL"]).rstrip("/")
    except Exception:
        pass
    return os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

FEATURES = {
    "home": {"label": "🏠 Command Center", "icon": "🏠"},
    "explain": {"label": "🔍 Explain Code", "icon": "🔍", "endpoint": "/explain"},
    "debug": {"label": "🐛 Debug Code", "icon": "🐛", "endpoint": "/debug"},
    "optimize": {"label": "⚡ Optimize", "icon": "⚡", "endpoint": "/optimize"},
    "refactor": {"label": "🔧 Refactor", "icon": "🔧", "endpoint": "/refactor"},
    "chat": {"label": "💬 Ask AI", "icon": "💬", "endpoint": "/chat"},
    "readme": {"label": "📄 README", "icon": "📄", "endpoint": "/generate-readme"},
    "commit": {"label": "📝 Commits", "icon": "📝", "endpoint": "/commit-message"},
    "complexity": {"label": "📊 Big-O", "icon": "📊", "endpoint": "/complexity"},
    "repo": {"label": "🗂️ Repo Scan", "icon": "🗂️", "endpoint": "/repo-summary"},
    "upload": {"label": "📁 Upload", "icon": "📁", "endpoint": "/upload-snippet"},
}

LANGUAGES = [
    "auto-detect", "Python", "JavaScript", "TypeScript", "Java",
    "Go", "C++", "C", "Rust", "SQL", "Shell", "Scala",
]

SAMPLES = {
    "Python — Buggy Fibonacci": '''def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))''',
    "JavaScript — Async bug": '''async function fetchUser(id) {
  const res = fetch(`https://api.example.com/users/${id}`);
  return res.json();
}''',
    "Python — Needs refactor": '''def p(d):
    r=[]
    for k,v in d.items():
        if v>0:
            r.append(k)
    return r''',
}

st.set_page_config(
    page_title="Neural Forge | AI Coding Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = get_backend_url()

st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
components.html(PARTICLE_HTML, height=0)

# ── Session state ───────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None


def inject_hero():
    st.markdown(HERO_HTML, unsafe_allow_html=True)


def backend_status() -> tuple[bool, dict]:
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200, r.json()
    except Exception:
        return False, {}


def post(endpoint: str, payload: dict, timeout: int = 90) -> str | None:
    try:
        resp = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json().get("response", "No response received.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot reach backend. Start it with: `uvicorn main:app --reload` in `backend/`")
    except requests.exceptions.Timeout:
        st.error("Request timed out — try a smaller snippet.")
    except requests.exceptions.HTTPError as e:
        detail = ""
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"API error: {detail}")
    except Exception as e:
        st.error(f"Error: {e}")
    return None


def add_history(feature: str, chars: int, elapsed: float):
    st.session_state.history.insert(0, {
        "feature": feature,
        "chars": chars,
        "elapsed": elapsed,
        "time": time.strftime("%H:%M:%S"),
    })
    st.session_state.history = st.session_state.history[:8]


def render_terminal_response(text: str, title: str = "NEURAL OUTPUT"):
    st.markdown(
        f"""
        <div class="terminal-header">
            <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown(text)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("⬇️ Download .md", text, file_name="neural_forge_output.md", use_container_width=True)
    with col2:
        if st.button("📋 Copy hint", use_container_width=True):
            st.info("Use the download button or select text from the markdown block above.")
    with col3:
        st.caption(f"{len(text):,} chars · ~{len(text.split())} words")


def run_analysis(endpoint: str, payload: dict, feature_name: str, code_len: int):
    progress = st.progress(0, text="Initializing neural link...")
    for i in range(25, 100, 25):
        time.sleep(0.08)
        progress.progress(i, text=f"Gemini processing... {i}%")
    t0 = time.time()
    result = post(endpoint, payload)
    elapsed = round(time.time() - t0, 2)
    progress.progress(100, text="Complete!")
    progress.empty()
    if result:
        st.session_state.last_response = result
        add_history(feature_name, code_len, elapsed)
        st.success(f"Analysis complete in **{elapsed}s**")
        render_terminal_response(result)
    return result


def code_workspace(key_prefix: str, default_height: int = 320) -> tuple[str, str]:
    col_code, col_meta = st.columns([4, 1])
    with col_meta:
        lang = st.selectbox("Language", LANGUAGES, key=f"{key_prefix}_lang")
        st.markdown('<div class="glass-panel"><h3>⚡ QUICK LOAD</h3></div>', unsafe_allow_html=True)
        sample_name = st.selectbox("Samples", ["—"] + list(SAMPLES.keys()), key=f"{key_prefix}_sample")
    with col_code:
        default = SAMPLES.get(sample_name, "") if sample_name != "—" else ""
        code = st.text_area(
            "Code input",
            value=default,
            height=default_height,
            placeholder="# Paste your code here — the forge awaits...",
            key=f"{key_prefix}_code",
            label_visibility="collapsed",
        )
    return code, lang


# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:12px 0;">
            <div style="font-family:Orbitron;font-size:1.1rem;font-weight:700;
                background:linear-gradient(90deg,#00f5ff,#a855f7);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                ⚡ NEURAL FORGE
            </div>
            <div style="font-family:JetBrains Mono;font-size:0.65rem;color:#64748b;margin-top:4px;">
                v2.0 · AI DEV COCKPIT
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    online, health = backend_status()
    if online:
        model = health.get("model", "gemini")
        st.markdown(
            f'<div class="status-online"><span class="pulse"></span> ONLINE · {model}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="status-offline">● OFFLINE</div>', unsafe_allow_html=True)
        st.caption(f"Expected: `{BACKEND_URL}`")

    st.divider()

    labels = [FEATURES[k]["label"] for k in FEATURES]
    keys = list(FEATURES.keys())
    idx = keys.index(st.session_state.page) if st.session_state.page in keys else 0
    choice = st.radio("Navigate", labels, index=idx, label_visibility="collapsed")
    st.session_state.page = keys[labels.index(choice)]

    st.divider()
    st.markdown("**Stack**")
    st.caption("FastAPI · Streamlit · Gemini · Docker")
    st.link_button("📚 API Docs", f"{BACKEND_URL}/docs", use_container_width=True)

    if st.session_state.history:
        st.divider()
        st.markdown("**Recent runs**")
        for h in st.session_state.history[:5]:
            st.caption(f"`{h['time']}` {h['feature']} · {h['elapsed']}s")


# ── Main content ────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    inject_hero()
    st.markdown(FEATURE_GRID_HTML, unsafe_allow_html=True)

    online, health = backend_status()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("API Status", "LIVE" if online else "DOWN")
    c2.metric("Model", health.get("model", "—") if online else "—")
    c3.metric("Endpoints", "11+" if online else "0")
    c4.metric("Session Runs", len(st.session_state.history))

    st.markdown('<div class="glass-panel"><h3>🎯 BUILT FOR AI-ENGINEERING ROLES</h3></div>', unsafe_allow_html=True)
    st.markdown("""
    **Neural Forge** is a full-stack AI developer tool demonstrating:

    - **REST API design** with FastAPI, Pydantic validation, Swagger docs, and CORS
    - **LLM integration** via Google Gemini for real-world dev workflows
    - **Containerized deployment** with Docker Compose and health checks
    - **AI-assisted productivity** — explain, debug, optimize, refactor, document, and analyze code

    Pick a module from the sidebar to begin. Paste code, upload files, or scan a mini-repo.
    """)

    st.markdown("### 🚀 Quick start")
    st.code("cd backend && uvicorn main:app --reload", language="bash")
    st.code("cd frontend && streamlit run app.py", language="bash")
    st.code("docker-compose up --build", language="bash")

    if st.session_state.last_response:
        st.divider()
        st.subheader("Last AI output")
        with st.expander("View", expanded=False):
            st.markdown(st.session_state.last_response)

elif page == "explain":
    inject_hero()
    st.markdown("### 🔍 Code Explainer")
    st.caption("Plain-English walkthrough with concepts and examples.")
    code, lang = code_workspace("explain")
    if st.button("⚡ EXPLAIN CODE", type="primary", use_container_width=True):
        if code.strip():
            run_analysis("/explain", {"code": code, "task": "Explain", "language": lang}, "Explain", len(code))
        else:
            st.warning("Paste code first.")

elif page == "debug":
    inject_hero()
    st.markdown("### 🐛 Debug Hunter")
    st.caption("Find bugs, root causes, and get fixed code.")
    code, lang = code_workspace("debug")
    if st.button("⚡ HUNT BUGS", type="primary", use_container_width=True):
        if code.strip():
            run_analysis("/debug", {"code": code, "task": "Debug", "language": lang}, "Debug", len(code))
        else:
            st.warning("Paste code first.")

elif page == "optimize":
    inject_hero()
    st.markdown("### ⚡ Performance Forge")
    st.caption("Optimize for speed, memory, and best practices.")
    code, lang = code_workspace("optimize")
    if st.button("⚡ OPTIMIZE", type="primary", use_container_width=True):
        if code.strip():
            run_analysis("/optimize", {"code": code, "task": "Optimize", "language": lang}, "Optimize", len(code))
        else:
            st.warning("Paste code first.")

elif page == "refactor":
    inject_hero()
    st.markdown("### 🔧 Refactor Studio")
    st.caption("Structured refactoring with trade-off analysis.")
    code, lang = code_workspace("refactor")
    goal = st.text_input("Refactoring goal", value="Improve readability, naming, and maintainability")
    if st.button("⚡ REFACTOR", type="primary", use_container_width=True):
        if code.strip():
            run_analysis(
                "/refactor",
                {"code": code, "goal": goal, "language": lang},
                "Refactor",
                len(code),
            )
        else:
            st.warning("Paste code first.")

elif page == "chat":
    inject_hero()
    st.markdown("### 💬 Pair Programmer")
    st.caption("Ask anything about your code — debugging hints, design, edge cases.")
    code, lang = code_workspace("chat", 260)
    question = st.text_area(
        "Your question",
        height=100,
        placeholder="Why does this fail on empty input? How would you add caching?",
    )
    if st.button("⚡ ASK NEURAL FORGE", type="primary", use_container_width=True):
        if code.strip() and question.strip():
            run_analysis(
                "/chat",
                {"code": code, "question": question, "language": lang},
                "Chat",
                len(code),
            )
        else:
            st.warning("Provide both code and a question.")

elif page == "readme":
    inject_hero()
    st.markdown("### 📄 README Generator")
    st.caption("Turn code or project notes into a production-ready README.")
    code = st.text_area("Project code or description", height=300, placeholder="# main.py, package.json, or project overview...")
    if st.button("⚡ GENERATE README", type="primary", use_container_width=True):
        if code.strip():
            run_analysis(
                "/generate-readme",
                {"code": code, "task": "README", "language": "auto-detect"},
                "README",
                len(code),
            )
        else:
            st.warning("Add content first.")

elif page == "commit":
    inject_hero()
    st.markdown("### 📝 Commit Message Forge")
    st.caption("Conventional Commits from your git diff.")
    diff = st.text_area("Git diff", height=300, placeholder="git diff output...\n+added\n-removed")
    if st.button("⚡ GENERATE COMMITS", type="primary", use_container_width=True):
        if diff.strip():
            t0 = time.time()
            result = post("/commit-message", {"diff": diff})
            if result:
                add_history("Commits", len(diff), round(time.time() - t0, 2))
                render_terminal_response(result, "COMMIT MESSAGES")
        else:
            st.warning("Paste a diff first.")

elif page == "complexity":
    inject_hero()
    st.markdown("### 📊 Complexity Analyzer")
    st.caption("Big-O time and space analysis with bottlenecks.")
    code, lang = code_workspace("complexity")
    if st.button("⚡ ANALYZE BIG-O", type="primary", use_container_width=True):
        if code.strip():
            t0 = time.time()
            result = post("/complexity", {"code": code, "language": lang})
            if result:
                add_history("Big-O", len(code), round(time.time() - t0, 2))
                render_terminal_response(result, "COMPLEXITY REPORT")
        else:
            st.warning("Paste code first.")

elif page == "repo":
    inject_hero()
    st.markdown("### 🗂️ Repo Architecture Scanner")
    st.caption("Paste up to 5 files — get architecture, data flow, and improvements.")
    files = {}
    tabs = st.tabs([f"File {i}" for i in range(1, 6)])
    for i, tab in enumerate(tabs, 1):
        with tab:
            fname = st.text_input("Filename", key=f"repo_fn_{i}", placeholder="backend/main.py")
            content = st.text_area("Content", key=f"repo_ct_{i}", height=140, placeholder="# paste file...")
            if fname.strip() and content.strip():
                files[fname.strip()] = content
    if st.button("⚡ SCAN REPOSITORY", type="primary", use_container_width=True):
        if files:
            total = sum(len(v) for v in files.values())
            run_analysis("/repo-summary", {"files": files}, f"Repo ({len(files)} files)", total)
        else:
            st.warning("Add at least one file with name and content.")

elif page == "upload":
    inject_hero()
    st.markdown("### 📁 File Upload Analyzer")
    st.caption("Drop source files — .py, .js, .ts, .java, .go, .rs, .cpp, .sql, .md")
    task = st.selectbox(
        "Analysis mode",
        ["Explain this code", "Debug this code", "Optimize this code", "Analyze complexity"],
    )
    uploaded = st.file_uploader(
        "Source file",
        type=["py", "js", "ts", "java", "go", "cpp", "c", "rs", "txt", "md", "sql"],
    )
    if uploaded:
        preview = uploaded.getvalue().decode("utf-8", errors="ignore")[:8000]
        st.markdown('<div class="glass-panel"><h3>📄 PREVIEW</h3></div>', unsafe_allow_html=True)
        st.code(preview, language=uploaded.name.split(".")[-1] if "." in uploaded.name else "text")
    if uploaded and st.button("⚡ ANALYZE FILE", type="primary", use_container_width=True):
        with st.spinner("Uploading to neural core..."):
            try:
                t0 = time.time()
                resp = requests.post(
                    f"{BACKEND_URL}/upload-snippet",
                    files={"file": (uploaded.name, uploaded.getvalue(), "text/plain")},
                    params={"task": task},
                    timeout=90,
                )
                resp.raise_for_status()
                result = resp.json().get("response")
                if result:
                    add_history(f"Upload {uploaded.name}", len(preview), round(time.time() - t0, 2))
                    render_terminal_response(result, f"FILE: {uploaded.name}")
            except Exception as e:
                st.error(f"Upload failed: {e}")

# Footer
st.markdown(
    """
    <div style="text-align:center;padding:24px 0 8px;font-family:JetBrains Mono;font-size:0.65rem;color:#475569;">
        NEURAL FORGE · FastAPI + Streamlit + Gemini · Built for AI-powered engineering workflows
    </div>
    """,
    unsafe_allow_html=True,
)
