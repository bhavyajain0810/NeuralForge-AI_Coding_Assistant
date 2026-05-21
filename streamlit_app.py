"""
Streamlit Cloud entry point (repo root).
Deploy settings: Main file = streamlit_app.py, Requirements = requirements.txt
"""

from pathlib import Path
import sys

_FRONTEND = Path(__file__).resolve().parent / "frontend"
if str(_FRONTEND) not in sys.path:
    sys.path.insert(0, str(_FRONTEND))

_app = _FRONTEND / "app.py"
_code = _app.read_text(encoding="utf-8")
exec(compile(_code, str(_app), "exec"), {"__name__": "__main__", "__file__": str(_app)})
