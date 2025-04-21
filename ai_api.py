# ai_api.py  – faster, lighter replacement (Python 3.9+)
import os, json, uuid, threading
from typing import Dict, List
import requests
from fastapi import FastAPI, HTTPException, Query

# ── read config.json exactly like before ─────────────────────────────────────
here      = os.path.dirname(__file__)
cfg_path  = os.path.join(here, "config.json")
if not os.path.exists(cfg_path):
    raise RuntimeError("Missing config.json – copy the template and fill it out.")

cfg          = json.load(open(cfg_path, "r", encoding="utf-8"))
OLLAMA_HOST  = cfg.get("ollama_host", "http://127.0.0.1:11434")  # NEW (optional)
OLLAMA_MODEL = cfg["ollama_model"]
HOST         = cfg.get("host", "127.0.0.1")
PORT         = cfg.get("port", 8000)
KEEPALIVE    = cfg.get("keep_alive", "1h")                       # keep model warm

app       = FastAPI()
_sessions: Dict[str, List[dict]] = {}            # {sid: [ {"role":...}, ... ]}
_lock     = threading.Lock()                     # protect _sessions in multithread

# ── helper ───────────────────────────────────────────────────────────────────
def chat_with_ollama(history: List[dict]) -> str:
    """Send the full history to Ollama’s /api/chat endpoint and return the reply."""
    payload = {
        "model":      OLLAMA_MODEL,
        "messages":   history,
        "stream":     False,          # oneshot response
        "keep_alive": KEEPALIVE,
    }
    try:
        r = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=300)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
    except requests.RequestException as e:
        raise HTTPException(500, f"Ollama error: {e}")

# ── /ask endpoint ────────────────────────────────────────────────────────────
@app.get("/ask")
def ask(query: str, session_id: str | None = Query(default=None)):
    # 1. get or create session
    if not session_id:
        session_id = str(uuid.uuid4())

    with _lock:
        history = _sessions.setdefault(session_id, [])

    # 2. append user turn → call Ollama
    history.append({"role": "user", "content": query})
    answer = chat_with_ollama(history)

    # 3. append assistant turn
    history.append({"role": "assistant", "content": answer})
    with _lock:
        _sessions[session_id] = history   # save updated history

    return {"response": answer, "session_id": session_id}

# ── run exactly like before ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
