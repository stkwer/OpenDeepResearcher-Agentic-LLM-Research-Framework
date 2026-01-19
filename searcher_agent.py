import os
from pprint import pprint

# from tavily import TavilyClient
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from planner_agent import planner_agent  # uses your existing planner

# Initialize Tavily client
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")

tavily_client = TavilySearch(tavily_api_key="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")

# ------------------------------------
# Lightweight Answer Generator (3–4 lines)
# ------------------------------------
answer_llm = ChatOpenAI(
    model="qwen2.5-7b-instruct",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0.2
)

answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
You are a research assistant.
Using the provided web snippets, answer the question clearly in 3–4 concise lines.
Do not mention sources or URLs.
Be factual and neutral.
"""),
    ("human",
     """
Question:
{question}

Web snippets:
{snippets}
""")
])

def searcher_agent(plan: dict, max_results: int = 3) -> dict:
    """
    Takes the planner output and runs Tavily search
    for each sub-question's `search_query`.
    Returns a new dict with search results attached.
    """
    if "sub_questions" not in plan:
        raise ValueError("Planner output missing 'sub_questions' key")

    enriched_sub_questions = []

    for sub in plan["sub_questions"]:
        search_query = sub.get("search_query") or sub.get("question")
        if not search_query:
            continue

        print(f"\n[Searcher] Searching for: {search_query}")

        # Tavily search call
        # search_response = tavily_client.search(
        #     query=search_query,
        #     max_results=max_results,      # keep small for speed
        #     search_depth="basic",         # "advanced" is slower, use only if needed
        #     include_raw_content=True,
        #     include_images=False,
        # )
        # results = search_response.get("results", [])
        raw_results = tavily_client.run(search_query, max_results=10)
        results = raw_results.get("results", [])

        snippets = "\n\n".join(
        r.get("content", "")[:500] for r in results[:2]
        )


        # Generate short answer
        chain = answer_prompt | answer_llm
        answer = chain.invoke({
            "question": sub["question"],
            "snippets": snippets
        }).content.strip()

        # Attach search results to this sub-question
        enriched_sub = {
            **sub,
            # "search_results": search_response.get("results", []),
            "short_answer": answer,
            "search_results": results
        }
        enriched_sub_questions.append(enriched_sub)

    return {
        "main_topic": plan.get("main_topic", ""),
        "sub_questions": enriched_sub_questions,
    }


if __name__ == "__main__":
    print("=== OpenDeepResearcher: Planner + Searcher ===")
    user_query = input("Enter your main research topic: ")

    # 1) PLAN
    print("\n[Planner] Generating sub-questions...")
    plan = planner_agent(user_query)

    print("\n[Planner] Sub-questions:")
    for sub in plan["sub_questions"]:
        print(f"  {sub['id']}. {sub['question']}")

    # 2) SEARCH
    print("\n[Searcher] Running Tavily searches for each sub-question...")
    research_results = searcher_agent(plan, max_results=3)

    # 3) Show a compact preview of the results
    print("\n=== Searcher Results (preview) ===")
    for sub in research_results["sub_questions"]:
        print(f"\n{sub['id']}. {sub['question']}")
        print(f"   search_query: {sub['search_query']}")
        print(f"   keywords    : {sub['keywords']}")
        print("  Answer  :")
        print(f"   {sub.get('short_answer', 'No answer generated.')}")
        for i, r in enumerate(sub["search_results"][:2], start=1):
            print(f"     {i}. {r.get('title', 'No title')} - {r.get('url', 'No URL')}")
