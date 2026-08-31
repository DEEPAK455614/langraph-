"""Simple LangGraph workflow: User Question -> Gemini LLM -> Answer."""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

load_dotenv()


class QAState(TypedDict):
    """State passed through the workflow."""
    question: str
    answer: str


def call_llm(state: QAState) -> dict:
    """Send the question from state to Gemini and return the answer."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Gemini API key not found. Create .env and add "
            "GOOGLE_API_KEY=your_key_here"
        )

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=0,
        max_retries=2,
        api_key=api_key,
        vertexai=False,
    )
    response = llm.invoke(state["question"])
    return {"answer": response.text}


def build_workflow():
    graph_builder = StateGraph(QAState)
    graph_builder.add_node("llm", call_llm)
    graph_builder.add_edge(START, "llm")
    graph_builder.add_edge("llm", END)
    return graph_builder.compile()


workflow = build_workflow()


def ask(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    result = workflow.invoke({"question": question, "answer": ""})
    return result["answer"]
