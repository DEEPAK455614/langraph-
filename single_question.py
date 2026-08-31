"""Ask one question through the compiled LangGraph workflow."""

from workflow import ask


def main() -> None:
    question = input("Question: ").strip()
    print(ask(question))


if __name__ == "__main__":
    main()
