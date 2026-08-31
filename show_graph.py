"""Print the compiled workflow as a Mermaid graph."""

from workflow import workflow


if __name__ == "__main__":
    print(workflow.get_graph().draw_mermaid())
