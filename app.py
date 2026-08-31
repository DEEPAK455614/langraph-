"""Interactive terminal interface for the LangGraph + Gemini workflow."""

from workflow import ask_question


def main() -> None:
    print("\n=== Simple LangGraph + Gemini Q&A ===")
    print("Flow: User Question -> Gemini LLM -> Answer")
    print("Type 'exit' to stop.\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            print("Please type a question.\n")
            continue
        try:
            print(f"Gemini: {ask_question(question)}\n")
        except Exception as exc:
            print(f"\nERROR: {exc}")
            print("Check your Gemini API key and internet connection.\n")


if __name__ == "__main__":
    main()
