"""Ask Gemini one question through the compiled LangGraph workflow."""
import argparse
from workflow import ask_question

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="*", help="Question to ask Gemini")
    args = parser.parse_args()
    question = " ".join(args.question).strip() or input("Question: ").strip()
    print(ask_question(question))

if __name__ == "__main__":
    main()
