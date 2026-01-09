from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

from agents.planner import PlannerAgent
from agents.searcher import SearcherAgent
from agents.writer import WriterAgent


# -----------------------------
# Shared State
# -----------------------------
class ResearchState(TypedDict):
    topic: str
    sub_questions: List[str]
    search_results: List[Dict[str, Any]]
    summary: str


# -----------------------------
# Agents
# -----------------------------
planner = PlannerAgent()
searcher = SearcherAgent()
writer = WriterAgent()


# -----------------------------
# Nodes
# -----------------------------
def planner_node(state: ResearchState):
    state["sub_questions"] = planner.run(state["topic"])
    return state


def searcher_node(state: ResearchState):
    results = []
    for q in state["sub_questions"]:
        results.extend(searcher.run(q))

    state["search_results"] = results
    return state


def writer_node(state: ResearchState):
    state["summary"] = writer.run(state["search_results"])
    return state


# -----------------------------
# Build Graph
# -----------------------------
def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("searcher", searcher_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
