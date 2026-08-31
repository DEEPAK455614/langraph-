"""Compile the workflow and display its Mermaid graph definition."""
from workflow import graph

def main() -> None:
    print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    main()
