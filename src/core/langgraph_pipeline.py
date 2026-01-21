from langgraph.graph import StateGraph
from src.agents.writer_agent import WriterAgent
from src.services.llm import get_llm


def build_graph():
    llm = get_llm()

    graph = StateGraph(dict)

    writer = WriterAgent(llm)

    graph.add_node("writer", writer.run)
    graph.set_entry_point("writer")

    return graph.compile()





























