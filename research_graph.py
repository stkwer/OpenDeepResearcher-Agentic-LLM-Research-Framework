from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from planner_agent import planner_agent
from searcher_agent import searcher_agent
from writer_agent import writer_agent


# ============================================================
# SHARED STATE (for LangGraph)
# ============================================================
class ResearchState(TypedDict):
    user_query: str
    plan: Dict[str, Any]
    research_results: Dict[str, Any]
    final_summary: str


# ============================================================
# LANGGRAPH NODES (NO PRINTING HERE)
# ============================================================
def planner_node(state: ResearchState) -> ResearchState:
    state["plan"] = planner_agent(state["user_query"])
    return state


def searcher_node(state: ResearchState) -> ResearchState:
    state["research_results"] = searcher_agent(
        state["plan"], max_results=3
    )
    return state


def writer_node(state: ResearchState) -> ResearchState:
    state["final_summary"] = writer_agent(
        state["research_results"]
    )
    return state


# ============================================================
# LANGGRAPH SETUP
# ============================================================
graph = StateGraph(ResearchState)

graph.add_node("planner", planner_node)
graph.add_node("searcher", searcher_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "searcher")
graph.add_edge("searcher", "writer")
graph.add_edge("writer", END)

research_graph = graph.compile()


# ============================================================
# MAIN EXECUTION (MATCH searcher_agent2.py OUTPUT EXACTLY)
# ============================================================
if __name__ == "__main__":
    print("=== OpenDeepResearcher: Planner + Searcher ===")

    user_query = input("Enter your main research topic: ")

    # ---------------- PLANNER ----------------
    print("\n[Planner] Generating sub-questions...")
    plan = planner_agent(user_query)

    print("\n[Planner] Sub-questions:")
    for sub in plan["sub_questions"]:
        print(f"  {sub['id']}. {sub['question']}")

    # ---------------- SEARCHER ----------------
    print("\n[Searcher] Running Tavily searches for each sub-question...")
    research_results = searcher_agent(plan, max_results=3)

    print("\n=== Searcher Results (preview) ===")
    for sub in research_results["sub_questions"]:
        print(f"\n{sub['id']}. {sub['question']}")
        print(f"   search_query: {sub['search_query']}")
        print(f"   keywords    : {sub['keywords']}")
        print("  Answer  :")
        print(f"   {sub.get('short_answer', 'No answer generated.')}")
        for i, r in enumerate(sub["search_results"][:2], start=1):
            print(f"     {i}. {r.get('title', 'No title')} - {r.get('url', 'No URL')}")

    # ---------------- WRITER ----------------
    print("\n================ FINAL RESEARCH REPORT ================\n")
    final_report = writer_agent(research_results)
    print(final_report)
