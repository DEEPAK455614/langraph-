"""Interactive terminal interface for the LangGraph + Gemini workflow."""

from workflow import ask


def main() -> None:
    print("=" * 60)
    print("LANGGRAPH + GEMINI QUESTION ANSWERING")
    print("Flow: User Question -> LLM -> Answer")
    print("Type 'exit' to close.")
    print("=" * 60)

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            print("Please enter a question.")
            continue

        try:
            print(f"\nGemini: {ask(question)}")
        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
