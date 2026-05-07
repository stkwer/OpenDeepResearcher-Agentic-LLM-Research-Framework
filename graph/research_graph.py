# from typing import Dict

# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent


# def run_research(topic: str) -> Dict:
#     """
#     Sequential agentic research pipeline:
#     Planner → Search → Writer
#     """

#     # 1️⃣ Planner
#     sub_questions = planner_agent(topic)

#     # 2️⃣ Searcher
#     sources = search_agent(sub_questions)

#     # 3️⃣ Writer
#     content_blocks = []
#     for q, items in sources.items():
#         content_blocks.append(q)
#         for item in items:
#             content_blocks.append(item["content"])

#     research_text = "\n".join(content_blocks)
#     final_report = writer_agent(topic, research_text)

#     return {
#         "topic": topic,
#         "sub_questions": sub_questions,
#         "search_results": sources,
#         "final_report": final_report
#     }



from typing import Dict
from planner import planner_agent
from search import search_agent
from writer import writer_agent

def run_research(topic: str) -> Dict:
    """
    Sequential agentic research pipeline:
    Planner → Search → Writer
    """
    # 1️⃣ Planner
    sub_questions = planner_agent(topic)

    # 2️⃣ Search
    sources = search_agent(sub_questions)

    # 3️⃣ Writer
    content_blocks = []
    all_sources = []  # Collect all sources for references
    
    for q, items in sources.items():
        content_blocks.append(q)
        for item in items:
            content_blocks.append(item["content"])
            # Collect source info for references
            if item.get("title") and item.get("url") and item.get("url").strip():
                all_sources.append({
                    "title": item["title"],
                    "url": item["url"]
                })

    research_text = "\n".join(content_blocks)
    final_report = writer_agent(topic, research_text)

    return {
        "topic": topic,
        "sub_questions": sub_questions,
        "search_results": sources,
        "final_report": final_report,
        "sources": all_sources  # Add sources for references
    }
