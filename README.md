# LocalAI Maltego Integration

This repository provides a local AI integration for Maltego using Ollama’s HTTP API via a FastAPI backend and a Python transform script. It supports multi turn, thread safe sessions and model warming for improved performance.

## Features

- **FastAPI server** querying Ollama’s HTTP `/api/chat` endpoint  
- **Configurable** via `config.json`:  
  - `ollama_model` – name of the Ollama model  
  - `ollama_host` – Ollama daemon’s HTTP address  
  - `host` & `port` – where to serve the FastAPI app  
  - `keep_alive` – how long to keep the model warm  
- **Thread safe** in memory session history per `session_id` (protected by `threading.Lock`)  
- **Model warming** with `keep_alive` to reduce cold start latency  
- **Maltego Transform** script (`ai_transform.py`) that:  
  1. Reads/writes `last_session.sid`  
  2. Calls `/ask` with the current session  
  3. Wraps the AI reply to 80 chars and emits valid Maltego XML  

## Prerequisites

- Python 3.9+  
- Ollama installed and running (e.g. `ollama daemon`)  
- Desired model loaded in Ollama (e.g. `dolphin-mixtral:8x7b`)  
- Maltego CE or Pro

## Installation

1. **Clone this repo**  
   ```bash
   git clone https://github.com/Beerrise/Maltego-Local-AI.git
   cd Maltego-Local-AI
   ```

2. **Configure**  
   Edit `config.json` with your ollama model:
   ```json
   {
     "ollama_model": "dolphin-mixtral:8x7b",
     "ollama_host":  "http://127.0.0.1:11434",
     "host":         "127.0.0.1",
     "port":         8000,
     "keep_alive":   "1h"
   }
   ```

3. **Install Python deps**  
   ```bash
   pip install fastapi uvicorn requests
   ```

## Running the API Server 

```bash
uvicorn ai_api:app
```
This reads your `config.json`, connects to Ollama’s HTTP API, and exposes `/ask`.

## Maltego Transform Setup

1. **Add a Local Transform**  
   - **Display Name**: `LocalAI` (or your choice)  
   - **Transform ID**: `local.ai`  
   - **Description**: `Local AI transform via Ollama HTTP API`  
   - **Input Entity Type**: `maltego.Phrase` (or your choice)

2. **Command Configuration**  
   - **Application**: `python`  
   - **Parameters**: `ai_transform.py`  
   - **Working Directory**: path to this repo  

3. **Permissions**  
   Ensure the transform folder is writable so `last_session.sid` can be created/updated.

## Usage

1. **Run a Query**  
   - Place a Phrase entity (e.g. `What is AI?`).  
   - Right click → Transforms → LocalAI.  
   - The AI’s response appears and `session_id` is saved.

2. **Follow up Queries**  
   - Add a new Phrase (e.g. `How does it work internally?`).  
   - Draw an arrow from the AI’s previous answer to this new Phrase.  
   - Run LocalAI again—context is preserved.

## Advanced & Tips

- **Multiple Sessions**: Duplicate the transform folder or adjust `ai_transform.py` to use custom `.sid` filenames for branching.  
- **Custom Prompts**: Modify `chat_with_ollama()` in `ai_api.py` to inject system or user prompts based on entity type.  
- **Production**: Behind Nginx or Caddy, enable CORS, TLS, and scale with Uvicorn/Gunicorn workers.

## Contributing

PRs and issues welcome! You might consider:  
- Database backed session storage  
- Prompt templating per entity type  
- Enhanced error handling and logging  

## License

MIT © Beerrise
