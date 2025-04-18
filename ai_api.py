import subprocess, uuid, json, os
from fastapi import FastAPI, Query
from typing import Dict

# load config.json from the same folder as this script
here = os.path.dirname(__file__)
cfg_path = os.path.join(here, "config.json")
if not os.path.exists(cfg_path):
    raise RuntimeError(f"Missing config.json — please copy template and fill it out.")

cfg = json.load(open(cfg_path, "r", encoding="utf-8"))
ollama_path  = cfg["ollama_path"]
ollama_model = cfg["ollama_model"]
HOST = cfg.get("host", "127.0.0.1")
PORT = cfg.get("port", 8000)

app = FastAPI()
sessions: Dict[str, str] = {}

def query_ollama(prompt: str) -> str:
    proc = subprocess.run(
        [ollama_path, "run", ollama_model],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if proc.returncode != 0:
        return f"Error: {proc.stderr}"
    return proc.stdout.strip()

@app.get("/ask")
def ask(query: str, session_id: str = Query(None)):
    import uuid as _uuid
    if not session_id or session_id not in sessions:
        session_id = str(_uuid.uuid4())
        sessions[session_id] = ""

    history = sessions[session_id]
    prompt  = (history + "\n" if history else "") + f"User: {query}\nAI:"
    answer  = query_ollama(prompt)
    sessions[session_id] = f"{prompt}{answer}"
    return {"response": answer, "session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)