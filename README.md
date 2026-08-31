# LangGraph + Gemini Simple Q&A

Required assignment flow:

User Question -> LLM -> Answer

## Setup

1. Open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:

   py -3.14 -m venv .venv

4. Activate on Windows PowerShell:

   .\\.venv\\Scripts\\Activate.ps1

   Or Command Prompt:

   .venv\\Scripts\\activate

5. Install packages:

   python -m pip install --upgrade pip
   pip install -r requirements.txt

6. Create a file called `.env`.

7. Put your NEW Gemini API key in it:

   GOOGLE_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.6-flash

8. Run:

   python app.py

For a single question: `python single_question.py "What is LangGraph?"`

To display the compiled graph: `python show_graph.py`

Example:

You: What is LangGraph?
Gemini: LangGraph is a framework for building stateful AI workflows...

Graph:

START -> llm -> END

State fields:
- question
- answer
