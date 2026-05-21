# Deploy Neural Forge

Streamlit Community Cloud hosts the **UI only**. The **FastAPI backend** must run separately (Render recommended).

---

## Step 1 — Push to GitHub

Repo: https://github.com/bhavyajain0810/NeuralForge-AI_Coding_Assistant

```bash
git add .
git commit -m "Add Streamlit Cloud and Render deployment config"
git push origin main
```

---

## Step 2 — Deploy backend on Render (free)

1. Go to [render.com](https://render.com) and sign in with GitHub.
2. **New** → **Blueprint** (or **Web Service**).
3. Connect repo `NeuralForge-AI_Coding_Assistant`.
4. If using **Blueprint**, Render reads `render.yaml` automatically.
5. If manual **Web Service**:
   - **Root Directory:** leave blank (repo root)
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`
6. Add environment variable:
   - `GEMINI_API_KEY` = your key from [Google AI Studio](https://aistudio.google.com/app/apikey)
7. Deploy and wait until **Live**.
8. Copy your service URL, e.g. `https://neural-forge-api.onrender.com`

Test:

```bash
curl https://YOUR-RENDER-URL.onrender.com/health
```

---

## Step 3 — Deploy frontend on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) (or [streamlit.io/cloud](https://streamlit.io/cloud)).
2. Sign in with **GitHub**.
3. Click **Create app** → **From existing repo**.
4. Select: `bhavyajain0810/NeuralForge-AI_Coding_Assistant`
5. Branch: `main`
6. **Main file path:** `streamlit_app.py`
7. **App URL:** pick a name, e.g. `neural-forge`
8. Click **Advanced settings**:
   - **Python version:** 3.11
   - **Requirements file:** `requirements.txt` (repo root)
9. Open **Secrets** and paste (replace with your Render URL):

```toml
BACKEND_URL = "https://neural-forge-api.onrender.com"
```

10. Click **Deploy**.

Your public app will be at:

`https://neural-forge.streamlit.app` (or the name you chose)

---

## Step 4 — Verify

1. Open the Streamlit app URL.
2. Sidebar should show **ONLINE** (green).
3. Try **Explain Code** with sample code.

If sidebar shows **OFFLINE**:

- Check `BACKEND_URL` secret (no trailing slash issues — app strips them).
- Render free tier **spins down** after inactivity; first request may take 30–60s.
- Confirm `GEMINI_API_KEY` is set on Render.

---

## Optional — Local secrets for testing

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit BACKEND_URL, then:
streamlit run streamlit_app.py
```

Never commit `secrets.toml` (it is in `.gitignore`).

---

## Resume links

| What | URL |
|------|-----|
| GitHub | https://github.com/bhavyajain0810/NeuralForge-AI_Coding_Assistant |
| Live demo | `https://YOUR-APP.streamlit.app` |
| API docs | `https://YOUR-RENDER-URL.onrender.com/docs` |
