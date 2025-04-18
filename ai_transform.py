import sys, os, requests, textwrap

# File to hold the last session the AI created
LAST_SESSION_FILE = "last_session.sid"

def load_last_session():
    try:
        return open(LAST_SESSION_FILE).read().strip()
    except FileNotFoundError:
        return None

def save_last_session(sid):
    with open(LAST_SESSION_FILE, "w") as f:
        f.write(sid)

def query_local_ai(query, session_id=None):
    params = {"query": query}
    if session_id:
        params["session_id"] = session_id
    r = requests.get("http://127.0.0.1:8000/ask", params=params)
    r.raise_for_status()
    return r.json()  # {"response": "...", "session_id": "UUID"}

def wrap(text):
    return "\n".join(textwrap.wrap(text, width=80))

if __name__ == "__main__":
    # 1) Get the new question from Maltego
    query = sys.argv[1] if len(sys.argv) > 1 else ""

    # 2) Load the last session ID (if any)
    last_sid = load_last_session()

    # 3) Call the API with that session ID
    result = query_local_ai(query, last_sid)
    answer    = result["response"]
    new_sid   = result["session_id"]

    # 4) Save the new session ID for the *next* query
    save_last_session(new_sid)

    # 5) Return a single Phrase entity with the wrapped answer
    wrapped = wrap(answer)
    print(f"""<MaltegoMessage>
<MaltegoTransformResponseMessage>
<Entities>
  <Entity Type="maltego.Phrase">
    <Value>{wrapped}</Value>
  </Entity>
</Entities>
</MaltegoTransformResponseMessage>
</MaltegoMessage>""")