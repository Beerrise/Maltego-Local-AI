# Changelog

All notable changes to **Maltego‑Local‑AI** will be documented in this file.

## [Unreleased] – 2025‑04‑21

### Added
- **keep_alive** setting in **config.json** to keep the Ollama model warmed between requests.  
- `chat_with_ollama()` helper in **ai_api.py** for clean, centralized HTTP calls to Ollama’s `/api/chat`.  
- Thread‑safe session storage using `threading.Lock` in **ai_api.py** to prevent race conditions under concurrency.  

### Changed
- **config.json**  
  - Renamed `ollama_path` → `ollama_host` (now targets Ollama’s HTTP API endpoint).  
  - Added `keep_alive` option; retained `ollama_model`, `host`, and `port`.  
- **ai_api.py**  
  - Switched from CLI/subprocess invocation to `requests.post()` against Ollama HTTP API.  
  - Refactored session management to append full chat history (`role` + `content`) per `session_id`.  
- **ai_transform.py**  
  - Output now wrapped in proper Maltego XML (`<MaltegoMessage>…</MaltegoMessage>`) for seamless graph integration.  
  - Persists `session_id` in a local `last_session.sid` file and wraps assistant responses at 80 chars for readability.  

### Deprecated
- Direct subprocess calls to the Ollama executable (fully replaced by HTTP API).  

### Fixed
- Cold‑start latency by introducing model warming via `keep_alive`.  
- Inconsistent session persistence across transform runs.  
- Potential threading issues when multiple `/ask` requests arrive simultaneously.  
