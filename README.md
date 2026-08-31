# LangGraph + Gemini Question Answering Workflow

A simple LangGraph workflow that receives a user question, sends it to Google Gemini, and returns the answer.

## Workflow

```text
START -> LLM Node -> END
```

- **State:** `QAState` stores the `question` and `answer`.
- **Node:** `call_llm` reads the question, calls Gemini, and returns the answer.
- **Edges:** `START -> llm -> END` define execution order.

## Setup on Windows

1. Clone or download this repository.
2. Open the folder in VS Code.
3. Create and activate a virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Copy `.env.example` to `.env`, then add your Gemini API key. Never commit `.env`.

## Run

```powershell
python app.py
```

One-question demo:

```powershell
python single_question.py
```

Print the workflow graph:

```powershell
python show_graph.py
```

## Demonstration video

https://www.loom.com/share/d05c8f1df43b4138b822b1211eeb4c81
