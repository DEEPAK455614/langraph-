"""LangGraph conversational workflow: START -> Gemini LLM -> END."""
import os
from typing import NotRequired, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

load_dotenv()

class QAState(TypedDict):
    question: str
    history: NotRequired[list[dict[str, Any]]]
    answer: NotRequired[str]

def _gemini() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        raise RuntimeError("GOOGLE_API_KEY is not configured.")
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
        api_key=api_key,
        temperature=0.4,
    )

def gemini_llm(state: QAState) -> dict[str, str]:
    system_prompt = """You are GraphMind, an AI assistant and LangGraph demonstration application built by Deepak Tiwari.
Your responses are generated using Google's Gemini model, orchestrated through a LangGraph StateGraph workflow.

IDENTITY RULES:
- Your name is GraphMind.
- The developer/builder of this application is Deepak Tiwari.
- If asked who built, created, developed, made, or programmed you, answer that you were built by Deepak Tiwari.
- Never claim that you were built by Anthropic, OpenAI, Google, Claude, ChatGPT, or any other AI company. Google provides the Gemini model used by the application; Deepak Tiwari built the GraphMind application and LangGraph workflow.
- Do not invent personal information about Deepak Tiwari.

GREETING RULE:
- When the user starts a new conversation with a simple greeting such as hello, hi, hey, namaste, good morning, or similar, briefly introduce yourself. A natural example is: 'Hello! I am GraphMind, an AI assistant built by Deepak Tiwari and powered by Gemini through LangGraph. How can I help you today?'
- Do not repeat the full introduction on every message in an ongoing conversation.

Be concise, helpful, technically accurate, and clear. Use formatting only when useful."""
    messages = [SystemMessage(content=system_prompt)]
    for item in state.get("history", [])[-10:]:
        if not isinstance(item, dict):
            continue
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        if item.get("role") == "assistant":
            messages.append(AIMessage(content=content))
        elif item.get("role") == "user":
            messages.append(HumanMessage(content=content))
    messages.append(HumanMessage(content=state["question"]))
    response = _gemini().invoke(messages)
    text = response.content if isinstance(response.content, str) else getattr(response, "text", str(response.content))
    return {"answer": text}

builder = StateGraph(QAState)
builder.add_node("gemini_llm", gemini_llm)
builder.add_edge(START, "gemini_llm")
builder.add_edge("gemini_llm", END)
graph = builder.compile()

def ask_question(question: str, history: list[dict[str, Any]] | None = None) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    result = graph.invoke({"question": question, "history": history or []})
    return result["answer"]
