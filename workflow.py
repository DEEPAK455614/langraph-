"""LangGraph workflow: START -> Gemini LLM -> END."""
import os
from typing import NotRequired
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

load_dotenv()

class QAState(TypedDict):
    question: str
    answer: NotRequired[str]

def _gemini() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        raise RuntimeError("GOOGLE_API_KEY is not configured. Add your Gemini API key to .env.")
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
        api_key=api_key,
    )

def gemini_llm(state: QAState) -> dict[str, str]:
    response = _gemini().invoke(state["question"])
    return {"answer": response.text}

builder = StateGraph(QAState)
builder.add_node("gemini_llm", gemini_llm)
builder.add_edge(START, "gemini_llm")
builder.add_edge("gemini_llm", END)
graph = builder.compile()

def ask_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    return graph.invoke({"question": question})["answer"]
