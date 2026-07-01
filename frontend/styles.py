"""Visual system for the Neural Forge Streamlit cockpit."""

GLOBAL_CSS = """
:root {
    --nf-bg: #050816;
    --nf-surface: #0b1022;
    --nf-panel: rgba(13, 20, 42, 0.88);
    --nf-panel-strong: rgba(8, 13, 30, 0.96);
    --nf-border: rgba(82, 211, 255, 0.18);
    --nf-border-strong: rgba(82, 211, 255, 0.34);
    --nf-text: #eef4ff;
    --nf-muted: #91a0bd;
    --nf-cyan: #52d3ff;
    --nf-purple: #9b7bff;
    --nf-pink: #ff6fcf;
    --nf-green: #42e8a4;
    --nf-yellow: #ffd166;
    --nf-red: #ff7185;
}

/* Remove Streamlit's application chrome without touching native sidebar controls. */
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
div[data-testid="stAppDeployButton"],
.stDeployButton,
#MainMenu,
footer {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="collapsedControl"] {
    z-index: 1001 !important;
}

.stApp {
    font-size: 0.94rem;
    color: var(--nf-text);
    background:
        radial-gradient(circle at 82% 2%, rgba(123, 92, 255, 0.18), transparent 30rem),
        radial-gradient(circle at 18% 32%, rgba(24, 185, 255, 0.08), transparent 28rem),
        linear-gradient(145deg, #050816 0%, #080b19 58%, #090615 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: 0.18;
    background-image:
        linear-gradient(rgba(82, 211, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(82, 211, 255, 0.08) 1px, transparent 1px);
    background-size: 52px 52px;
    mask-image: linear-gradient(to bottom, black, transparent 78%);
}

.block-container {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 1440px;
    margin-inline: auto;
    padding: 0.65rem 1.5rem 2.4rem;
}

[data-testid="stAppViewContainer"] > .main {
    width: 100%;
    min-width: 0;
    flex: 1 1 auto;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

h1, h2, h3, h4 {
    color: var(--nf-text);
    letter-spacing: -0.025em;
}

p, label, [data-testid="stCaptionContainer"] {
    line-height: 1.58;
}

.nf-hero {
    position: relative;
    overflow: hidden;
    min-height: 218px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 1.75rem 2.1rem;
    margin-bottom: 0.7rem;
    border: 1px solid var(--nf-border-strong);
    border-radius: 24px;
    background:
        linear-gradient(115deg, rgba(10, 17, 39, 0.98), rgba(18, 12, 43, 0.92)),
        var(--nf-panel-strong);
    box-shadow:
        0 24px 70px rgba(0, 0, 0, 0.38),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.nf-hero::before {
    content: "";
    position: absolute;
    width: 430px;
    height: 430px;
    top: -260px;
    right: -90px;
    border-radius: 50%;
    border: 1px solid rgba(82, 211, 255, 0.25);
    box-shadow:
        0 0 0 48px rgba(155, 123, 255, 0.035),
        0 0 0 96px rgba(82, 211, 255, 0.025);
}

.nf-hero::after {
    content: "</>";
    position: absolute;
    right: 6%;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(82, 211, 255, 0.09);
    font: 800 clamp(4rem, 9vw, 7.5rem) ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: -0.12em;
}

.nf-eyebrow {
    position: relative;
    z-index: 1;
    margin-bottom: 0.45rem;
    color: var(--nf-cyan);
    font: 700 0.74rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.17em;
    text-transform: uppercase;
}

.nf-title {
    position: relative;
    z-index: 1;
    max-width: 800px;
    margin: 0;
    font-size: clamp(2.25rem, 4.5vw, 3.75rem);
    font-weight: 850;
    letter-spacing: -0.065em;
    line-height: 0.94;
    color: #f7fbff;
    text-shadow: 0 0 38px rgba(82, 211, 255, 0.16);
}

.nf-subtitle {
    position: relative;
    z-index: 1;
    max-width: 740px;
    margin: 0.7rem 0 0.85rem;
    color: #b4c1da;
    font-size: 0.96rem;
}

.nf-badges {
    position: relative;
    z-index: 1;
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
}

.nf-badge {
    padding: 0.3rem 0.62rem;
    border: 1px solid rgba(82, 211, 255, 0.28);
    border-radius: 999px;
    background: rgba(82, 211, 255, 0.07);
    color: #9be7ff;
    font: 650 0.72rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.05em;
}

.nf-badge.purple {
    border-color: rgba(155, 123, 255, 0.34);
    background: rgba(155, 123, 255, 0.09);
    color: #c7b7ff;
}

.nf-badge.pink {
    border-color: rgba(255, 111, 207, 0.3);
    background: rgba(255, 111, 207, 0.08);
    color: #ffabe2;
}

.nf-feature-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.58rem;
    margin: 0.55rem 0 1rem;
}

.nf-feature {
    position: relative;
    overflow: hidden;
    min-height: 106px;
    padding: 0.72rem 0.78rem;
    border: 1px solid var(--nf-border);
    border-radius: 15px;
    background: linear-gradient(145deg, rgba(14, 22, 47, 0.92), rgba(9, 14, 31, 0.92));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
    transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

.nf-feature:hover {
    transform: translateY(-3px);
    border-color: var(--nf-border-strong);
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.23);
}

.nf-feature-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.82rem;
    height: 1.82rem;
    margin-bottom: 0.48rem;
    border: 1px solid rgba(82, 211, 255, 0.22);
    border-radius: 10px;
    background: rgba(82, 211, 255, 0.09);
    color: var(--nf-cyan);
    font: 750 0.78rem ui-monospace, SFMono-Regular, Consolas, monospace;
}

.nf-feature strong {
    display: block;
    margin-bottom: 0.2rem;
    color: #f0f6ff;
    font-size: 0.84rem;
}

.nf-feature span {
    display: block;
    color: var(--nf-muted);
    font-size: 0.7rem;
    line-height: 1.34;
}

.nf-page-heading {
    position: relative;
    overflow: hidden;
    margin-bottom: 0.75rem;
    padding: 1rem 1.2rem;
    border: 1px solid var(--nf-border);
    border-radius: 17px;
    background: linear-gradient(120deg, rgba(13, 22, 48, 0.94), rgba(19, 13, 42, 0.86));
}

.nf-page-heading::after {
    content: "";
    position: absolute;
    width: 170px;
    height: 170px;
    right: -75px;
    top: -95px;
    border-radius: 50%;
    background: rgba(155, 123, 255, 0.12);
    filter: blur(4px);
}

.nf-page-kicker {
    margin-bottom: 0.35rem;
    color: var(--nf-cyan);
    font: 700 0.68rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.nf-page-heading h2 {
    margin: 0 0 0.3rem;
    color: #f7faff;
    font-size: 1.48rem;
}

.nf-page-heading p {
    max-width: 820px;
    margin: 0;
    color: var(--nf-muted);
}

.nf-section-label {
    margin: 0.85rem 0 0.48rem;
    color: #dbe8ff;
    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.nf-response-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.9rem;
    color: #f5f8ff;
    font-size: 1rem;
    font-weight: 760;
}

.nf-response-dot {
    width: 0.62rem;
    height: 0.62rem;
    border-radius: 50%;
    background: var(--nf-green);
    box-shadow: 0 0 0 5px rgba(66, 232, 164, 0.1), 0 0 18px rgba(66, 232, 164, 0.45);
}

.nf-status {
    display: inline-flex;
    align-items: center;
    gap: 0.48rem;
    padding: 0.42rem 0.7rem;
    border-radius: 999px;
    font: 700 0.72rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.03em;
}

.nf-status::before {
    content: "";
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 12px currentColor;
}

.nf-status.online {
    border: 1px solid rgba(66, 232, 164, 0.3);
    background: rgba(66, 232, 164, 0.09);
    color: #67f0b8;
}

.nf-status.degraded {
    border: 1px solid rgba(255, 209, 102, 0.3);
    background: rgba(255, 209, 102, 0.08);
    color: #ffe092;
}

.nf-status.offline {
    border: 1px solid rgba(255, 113, 133, 0.3);
    background: rgba(255, 113, 133, 0.08);
    color: #ff91a1;
}

.nf-side-brand {
    padding: 0.15rem 0 0.42rem;
}

.nf-side-logo {
    color: #f2f7ff;
    font-size: 1.1rem;
    font-weight: 850;
    letter-spacing: -0.035em;
}

.nf-side-logo span {
    color: var(--nf-cyan);
}

.nf-side-sub {
    margin-top: 0.2rem;
    color: #697895;
    font: 600 0.65rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.11em;
    text-transform: uppercase;
}

[data-testid="stSidebar"] {
    width: 288px !important;
    min-width: 288px !important;
    max-width: min(288px, 82vw) !important;
    border-right: 1px solid rgba(82, 211, 255, 0.16);
    background:
        radial-gradient(circle at 20% 5%, rgba(82, 211, 255, 0.08), transparent 15rem),
        linear-gradient(180deg, #080d1d, #090717);
}

[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    flex-basis: 0 !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 0.8rem 0.78rem 1.25rem;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 0;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    min-height: 0;
    padding: 0.27rem 0.42rem;
    border: 1px solid transparent;
    border-radius: 9px;
    color: #aebbd2;
    transition: background 140ms ease, border-color 140ms ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #aebbd2 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    border-color: rgba(82, 211, 255, 0.22);
    background: rgba(82, 211, 255, 0.075);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #eef6ff !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: rgba(82, 211, 255, 0.15);
    background: rgba(82, 211, 255, 0.06);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.78rem;
}

[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stLinkButton > a {
    min-height: 2.05rem;
    padding-block: 0.28rem;
    font-size: 0.78rem;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input,
[data-baseweb="select"] > div {
    border-color: rgba(104, 132, 180, 0.28) !important;
    background: rgba(4, 9, 23, 0.72) !important;
    color: #dce9ff !important;
}

[data-testid="stTextArea"] textarea {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
    font-size: 0.84rem;
    line-height: 1.56;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(82, 211, 255, 0.56) !important;
    box-shadow: 0 0 0 2px rgba(82, 211, 255, 0.1) !important;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

.stButton > button[kind="primary"] {
    border: 0;
    background: linear-gradient(110deg, #39c8f5, #8266f4 62%, #b65ee4);
    box-shadow: 0 10px 28px rgba(77, 96, 240, 0.24);
    color: #050816;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(110deg, #68dcff, #9c83ff 62%, #d17af4);
    box-shadow: 0 13px 34px rgba(82, 211, 255, 0.2);
    transform: translateY(-1px);
}

.stButton > button:not([kind="primary"]),
[data-testid="stDownloadButton"] button,
.stLinkButton a {
    border-color: rgba(82, 211, 255, 0.2);
    background: rgba(11, 18, 39, 0.74);
    color: #b9c8e1;
}

[data-testid="stMetric"] {
    min-height: 88px;
    padding: 0.68rem 0.8rem;
    border: 1px solid var(--nf-border);
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(13, 21, 45, 0.9), rgba(8, 13, 29, 0.9));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

[data-testid="stMetricValue"] {
    color: #f5f8ff;
    font-size: 1.16rem;
}

[data-testid="stMetricLabel"] {
    color: #8190ad;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--nf-border) !important;
    border-radius: 15px !important;
    background: linear-gradient(145deg, rgba(13, 21, 45, 0.78), rgba(8, 13, 29, 0.8));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

[data-testid="stCode"] {
    border: 1px solid rgba(82, 211, 255, 0.14);
    border-radius: 10px;
}

.nf-footer {
    margin-top: 1.6rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(82, 211, 255, 0.12);
    color: #60708e;
    font: 600 0.7rem ui-monospace, SFMono-Regular, Consolas, monospace;
    letter-spacing: 0.05em;
    text-align: center;
}

@media (max-width: 1180px) {
    .nf-feature-grid {
        grid-template-columns: repeat(5, minmax(0, 1fr));
    }

    .nf-hero::after {
        opacity: 0.5;
    }
}

@media (max-width: 1040px) {
    .block-container {
        padding: 1rem 1.1rem 2rem;
    }

    .nf-feature-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .nf-title {
        font-size: clamp(2.1rem, 5vw, 3.15rem);
    }
}

@media (max-width: 800px) {
    .block-container {
        padding: 0.85rem 0.8rem 1.8rem;
    }

    .nf-feature-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .nf-hero {
        min-height: 195px;
        padding: 1.35rem 1.25rem;
    }

    .nf-hero::after {
        display: none;
    }
}

@media (max-width: 520px) {
    .nf-feature-grid {
        grid-template-columns: 1fr;
    }

    .nf-hero {
        border-radius: 18px;
        padding: 1.15rem 1rem;
    }
}
"""

HERO_HTML = """
<section class="nf-hero">
  <div class="nf-eyebrow">AI developer command center // system ready</div>
  <h1 class="nf-title">Neural Forge</h1>
  <p class="nf-subtitle">
    A full-stack AI coding cockpit for understanding code, hunting defects,
    improving performance, and turning engineering context into work you can ship.
  </p>
  <div class="nf-badges">
    <span class="nf-badge">FASTAPI</span>
    <span class="nf-badge purple">GOOGLE GEMINI</span>
    <span class="nf-badge pink">STREAMLIT</span>
    <span class="nf-badge">DOCKER</span>
  </div>
</section>
"""

FEATURE_GRID_HTML = """
<div class="nf-feature-grid">
  <div class="nf-feature"><div class="nf-feature-icon">EX</div><strong>Explain Code</strong><span>Clear walkthroughs, concepts, and examples.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">DB</div><strong>Debug Code</strong><span>Root causes, fixes, and prevention guidance.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">OP</div><strong>Optimize</strong><span>Performance, memory, and best-practice review.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">RF</div><strong>Refactor</strong><span>Cleaner structure with explicit trade-offs.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">AI</div><strong>Ask AI</strong><span>Focused pair-programming questions.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">MD</div><strong>README</strong><span>Professional project documentation.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">GT</div><strong>Commits</strong><span>Ranked Conventional Commit messages.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">O(n)</div><strong>Big-O</strong><span>Time, space, and bottleneck analysis.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">RP</div><strong>Repo Scan</strong><span>Architecture and multi-file insight.</span></div>
  <div class="nf-feature"><div class="nf-feature-icon">UP</div><strong>Upload</strong><span>Analyze supported source files directly.</span></div>
</div>
"""
