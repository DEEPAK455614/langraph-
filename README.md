# GraphMind — LangGraph × Gemini

A polished conversational AI demo built with LangGraph, LangChain, Google Gemini, Flask, and Render.

## Workflow

`START → User Question → Gemini LLM node → Answer → END`

The browser sends the user's message to `/api/chat`. The Flask backend passes it into a compiled LangGraph `StateGraph`; the Gemini node generates the response and the graph returns it to the UI.

## Features

- Premium responsive chat interface
- Conversational context for follow-up questions
- Explicit LangGraph workflow visualization
- Server-side Gemini API key handling
- Health endpoint for deployment monitoring
- Render-ready Gunicorn configuration
- Mobile-friendly interview/demo experience

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Put your Gemini key in .env
python app.py
```

Open `http://localhost:10000`.

## Environment variables

- `GOOGLE_API_KEY` — required, keep secret
- `GEMINI_MODEL` — defaults to `gemini-3.7-flash`

## Production

Build: `pip install -r requirements.txt`

Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
