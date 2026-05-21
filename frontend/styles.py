"""Neural Forge — cyberpunk glass UI styles for Streamlit."""

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 1.5rem !important; max-width: 1400px !important; }

/* ── Animated cosmic background ── */
.stApp {
    background: #050508;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0, 245, 255, 0.15), transparent),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(191, 0, 255, 0.12), transparent),
        radial-gradient(ellipse 50% 30% at 50% 50%, rgba(255, 0, 170, 0.06), transparent),
        linear-gradient(180deg, #050508 0%, #0a0612 40%, #060a14 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
    animation: gridDrift 20s linear infinite;
}

@keyframes gridDrift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(48px, 48px); }
}

/* ── Typography ── */
.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(2rem, 5vw, 3.2rem) !important;
    font-weight: 900 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, #00f5ff 0%, #a855f7 45%, #ff00aa 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    filter: drop-shadow(0 0 30px rgba(0, 245, 255, 0.35));
    margin: 0 0 0.25rem 0 !important;
    line-height: 1.1 !important;
}

.hero-sub {
    font-family: 'Space Grotesk', sans-serif !important;
    color: rgba(200, 220, 255, 0.75) !important;
    font-size: 1.05rem !important;
    margin: 0 0 1rem 0 !important;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0 20px 0;
}

.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid rgba(0, 245, 255, 0.35);
    background: rgba(0, 245, 255, 0.08);
    color: #00f5ff;
    letter-spacing: 0.05em;
}

.badge.purple { border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.1); color: #c084fc; }
.badge.pink { border-color: rgba(255, 0, 170, 0.35); background: rgba(255, 0, 170, 0.08); color: #f472b6; }

/* ── Glass panels ── */
.glass-panel {
    background: rgba(12, 14, 28, 0.65);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(0, 245, 255, 0.18);
    border-radius: 20px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.45),
        inset 0 1px 0 rgba(255, 255, 255, 0.06),
        0 0 60px rgba(0, 245, 255, 0.04);
}

.glass-panel h3 {
    font-family: 'Orbitron', sans-serif;
    color: #e0e7ff;
    font-size: 0.95rem;
    margin: 0 0 0.5rem 0;
    letter-spacing: 0.06em;
}

/* ── Feature cards (HTML) ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 10px;
    margin: 16px 0;
}

.feat-card {
    font-family: 'Space Grotesk', sans-serif;
    text-align: center;
    padding: 14px 8px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    color: #94a3b8;
    font-size: 0.78rem;
    transition: all 0.25s ease;
}

.feat-card:hover {
    border-color: rgba(0, 245, 255, 0.4);
    background: rgba(0, 245, 255, 0.06);
    color: #00f5ff;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 245, 255, 0.15);
}

.feat-card .icon { font-size: 1.6rem; display: block; margin-bottom: 6px; }

/* ── Terminal response box ── */
.terminal-out {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.55;
    color: #86efac;
    background: rgba(0, 0, 0, 0.55);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    max-height: 520px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

.terminal-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #00f5ff;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.dot.r { background: #ff5f57; }
.dot.y { background: #febc2e; }
.dot.g { background: #28c840; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(5, 5, 12, 0.98) 0%, rgba(15, 8, 30, 0.98) 100%) !important;
    border-right: 1px solid rgba(0, 245, 255, 0.2) !important;
}

[data-testid="stSidebar"] .stRadio > label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #cbd5e1 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 50%, #ff00aa 100%) !important;
    color: #050508 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.65rem 1.5rem !important;
    box-shadow: 0 0 28px rgba(0, 245, 255, 0.35), 0 4px 20px rgba(0,0,0,0.4) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 0 48px rgba(168, 85, 247, 0.5) !important;
}

.stButton > button:not([kind="primary"]) {
    font-family: 'Space Grotesk', sans-serif !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0, 245, 255, 0.25) !important;
    color: #94a3b8 !important;
    border-radius: 10px !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(0, 0, 0, 0.45) !important;
    border: 1px solid rgba(0, 245, 255, 0.25) !important;
    border-radius: 12px !important;
    color: #a7f3d0 !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(168, 85, 247, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f5ff !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #64748b !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'Space Grotesk', sans-serif !important;
    background: rgba(0, 245, 255, 0.05) !important;
    border-radius: 10px !important;
}

/* ── Status pills ── */
.status-online {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #4ade80;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
}

.status-offline {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #f87171;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
}

.pulse {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4ade80;
    animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.6); }
    50% { opacity: 0.7; box-shadow: 0 0 0 8px rgba(74, 222, 128, 0); }
}

/* ── Scan line overlay (subtle) ── */
.scanline {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.4), transparent);
    animation: scan 4s linear infinite;
    pointer-events: none;
    z-index: 9999;
    opacity: 0.5;
}

@keyframes scan {
    0% { top: -2px; }
    100% { top: 100vh; }
}
"""

PARTICLE_HTML = """
<div class="scanline"></div>
<canvas id="neural-particles" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.35;"></canvas>
<script>
(function() {
  const c = document.getElementById('neural-particles');
  if (!c) return;
  const ctx = c.getContext('2d');
  let w, h, pts = [];
  function resize() {
    w = c.width = window.innerWidth;
    h = c.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);
  for (let i = 0; i < 80; i++) {
    pts.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.5
    });
  }
  function draw() {
    ctx.clearRect(0, 0, w, h);
    pts.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = i % 3 === 0 ? 'rgba(0,245,255,0.6)' : (i % 3 === 1 ? 'rgba(168,85,247,0.5)' : 'rgba(255,0,170,0.4)');
      ctx.fill();
      pts.slice(i + 1, i + 6).forEach(q => {
        const d = Math.hypot(p.x - q.x, p.y - q.y);
        if (d < 120) {
          ctx.strokeStyle = 'rgba(0,245,255,' + (1 - d/120) * 0.15 + ')';
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.stroke();
        }
      });
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
"""

HERO_HTML = """
<div class="hero-title">⚡ NEURAL FORGE</div>
<p class="hero-sub">AI-powered developer cockpit — debug, explain, refactor & ship faster</p>
<div class="badge-row">
  <span class="badge">FASTAPI</span>
  <span class="badge purple">GEMINI 1.5</span>
  <span class="badge pink">STREAMLIT</span>
  <span class="badge">DOCKER</span>
</div>
"""

FEATURE_GRID_HTML = """
<div class="feature-grid">
  <div class="feat-card"><span class="icon">🔍</span>Explain</div>
  <div class="feat-card"><span class="icon">🐛</span>Debug</div>
  <div class="feat-card"><span class="icon">⚡</span>Optimize</div>
  <div class="feat-card"><span class="icon">🔧</span>Refactor</div>
  <div class="feat-card"><span class="icon">💬</span>Ask AI</div>
  <div class="feat-card"><span class="icon">📄</span>README</div>
  <div class="feat-card"><span class="icon">📝</span>Commits</div>
  <div class="feat-card"><span class="icon">📊</span>Big-O</div>
  <div class="feat-card"><span class="icon">🗂️</span>Repo Scan</div>
  <div class="feat-card"><span class="icon">📁</span>Upload</div>
</div>
"""
