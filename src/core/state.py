from typing import TypedDict, List, Dict


class GraphState(TypedDict, total=False):
    input: str

    planner_steps: List[str]
    sub_questions: List[str]

    search_results: List[Dict[str, str]]
    sources: List[Dict[str, str]]

    final_answer: str
    final_output: str






