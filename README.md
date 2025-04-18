# LocalAI Maltego Integration

This repository provides a local AI integration for Maltego using Ollama via a FastAPI backend and a Python transform script. 
It maintains context between queries in a linear session, allowing follow-up questions to build upon previous answers.

## Features

- Local FastAPI server querying Ollama models
- Configurable Ollama path and model via `config.json`
- Linear session context stored in `last_session.sid`
- Maltego Local Transform for contextual AI responses

## Prerequisites

- **Windows** (tested on Windows 10/11)
- **Python 3.8+** installed and added to PATH
- **Ollama** installed and configured with your desired model (e.g., `dolphin-mixtral:8x7b`)
- **Maltego** (Tested on Community Edition)

## Installation

1. **Download this repository**
	- Put config.json and ai_api.py into your .ollama folder (e.g., `C:\Users\YourUserNameHere\.ollama`)
	- Put ai_transform.py anywhere you'd like. (e.g., `C:\Users\YourUsernameHere\Documents\Maltego_Transforms`)
2. **Edit config.json**``:

   ```json
   {
     "ollama_path": "C:\\Users\\<USERNAME>\\AppData\\Local\\Programs\\Ollama\\ollama.exe",
     "ollama_model": "dolphin-mixtral:8x7b",
     "host": "127.0.0.1",
     "port": 8000
   }
   ```

   - Fill in the correct path/model you are using.

3. **Install Python dependencies**:

   ```powershell
   pip install fastapi uvicorn requests
   ```

## Running the FastAPI Server

In Powershell or command prompt, CD into .ollama folder under `C:\Users\YourUserNameHere\.ollama` 
Start the local AI API server:

```powershell
uvicorn ai_api:app --reload
```

This will read your `config.json`, launch your selected AI Model via Ollama, and expose `/ask` for queries.

## Maltego Transform Setup

- Open **Maltego → Top Left → New Local Transform**

### Configure Details

- **Display Name**: LocalAI (`Or Anything you'd like`)
- **Transform ID**: local.ai (`Or Anything you'd like`)
- **Description**: Local AI transform
- **Input Entity Type**: `maltego.Phrase`

**You can add a new transform and select maltego.IPv4Address, maltego.website, etc etc under Input Entity Type for different entities**

### Command Line

- **Command**: `python` (your Python interpreter)
- **Parameters**: `ai_transform.py`
- **Working Directory**: `<ai.transform.py repository root>`

### Parameter Mapping

No additional parameters needed—Maltego will pass the current Phrase text as `sys.argv[1]` to `ai_transform.py`.

Click **Finish** to save the transform.

## Usage

1. **Ask a question**: Add a Phrase entity (e.g., `What is life?`), right-click it, and run **LocalAI (linear session)**.
2. **Follow up**: Add another Phrase (e.g., `What is the meaning of life?`), draw an arrow **from** the AI’s answer **to** the new Phrase, and run the same transform. The AI will remember its previous answer and respond with context.

## Notes

- This integration uses a simple linear session stored in `last_session.sid`. It supports single-threaded follow-ups.
- For branching sessions or multiple simultaneous contexts, consider extending to a full session store or using Maltego Pro’s parameter mappings.

## Contributing

Feel free to open issues or submit pull requests for enhancements, such as:

- Branching session support
- Custom prompts per entity type
- Persistent database storage for sessions

## License

MIT © Beerrise
