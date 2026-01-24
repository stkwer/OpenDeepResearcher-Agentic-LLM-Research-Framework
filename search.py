from dotenv import load_dotenv
import os
from typing import List, Dict
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file.")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search_agent(
    sub_questions: List[str],
    max_results_per_query: int = 1
) -> Dict[str, List[Dict]]:
    """
    Search Agent (Fast Mode):
    - Only 1 result per question for speed
    - Short content snippets
    """

    results: Dict[str, List[Dict]] = {}

    for question in sub_questions:
        try:
            response = tavily.search(
                query=question,
                max_results=max_results_per_query,
                search_depth="basic",
                include_answer=False,
                include_raw_content=False,
                timeout=5
            )

            items = response.get("results", [])

            clean_items = []
            for item in items:
                clean_items.append({
                    "title": item.get("title", "Unknown Source"),
                    "url": item.get("url", ""),
                    "content": (item.get("content") or "")[:150]
                })

            results[question] = clean_items

        except Exception as e:
            results[question] = [{
                "title": "Search Error",
                "url": "",
                "content": str(e)
            }]

    return results



































































# # Integrated
# # from dotenv import load_dotenv
# # import os
# # from typing import List, Dict
# # from tavily import TavilyClient

# # # Load environment variables
# # load_dotenv()
# # TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# # if not TAVILY_API_KEY:
# #     raise ValueError("TAVILY_API_KEY not found. Please add it to your .env file.")

# # # Initialize Tavily client
# # tavily = TavilyClient(api_key=TAVILY_API_KEY)

# # def search_agent(
# #     sub_questions: List[str],
# #     max_results_per_query: int = 3,
# #     search_depth: str = "basic"
# # ) -> Dict[str, List[Dict]]:
# #     """
# #     Search Agent:
# #     Takes a list of sub-questions, fetches search results from Tavily,
# #     and returns structured results as a dictionary.
# #     """
# #     all_results = {}
# #     for question in sub_questions:
# #         try:
# #             response = tavily.search(
# #                 query=question,
# #                 max_results=max_results_per_query,
# #                 search_depth=search_depth,
# #                 include_answer=False,
# #                 include_raw_content=False,
# #                 timeout=8
# #             )
# #             all_results[question] = response.get("results", [])
# #         except Exception as e:
# #             all_results[question] = [{"error": str(e)}]
# #     return all_results

# # # Example usage
# # if __name__ == "__main__":
# #     # Example sub-questions (replace with your planner output)
# #     sub_questions = [
# #         "What is LangGraph?",
# #         "What are the security risks of autonomous LLM agents?"
# #     ]
# #     results = search_agent(sub_questions)

# #     # Display results
# #     for question, items in results.items():
# #         print(f"\n=== {question} ===")
# #         for item in items:
# #             title = item.get("title", "No title")
# #             url = item.get("url", "No URL")
# #             score = item.get("score", "N/A")
# #             print(f"- {title} | {url} | Score: {score}")



# from dotenv import load_dotenv
# import os
# from typing import List, Dict
# from tavily import TavilyClient

# load_dotenv()

# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY not found. Please add it to your .env file.")

# tavily = TavilyClient(api_key=TAVILY_API_KEY)

# def search_agent(sub_questions: List[str], max_results_per_query: int = 2) -> Dict[str, List[Dict]]:
#     """
#     Search Agent:
#     Fetches top N results for each sub-question from Tavily.
#     Snippets truncated to speed up processing.
#     """

#     results = {}
#     for question in sub_questions:
#         try:
#             response = tavily.search(
#                 query=question,
#                 max_results=max_results_per_query,
#                 search_depth="basic",
#                 include_answer=False,
#                 include_raw_content=False,
#                 timeout=5
#             )
#             results[question] = response.get("results", [])
#         except Exception as e:
#             results[question] = [{"error": str(e)}]
#     return results



# # search.py
# from dotenv import load_dotenv
# import os
# from typing import List, Dict
# from tavily import TavilyClient

# load_dotenv()
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY not found in .env file.")

# tavily = TavilyClient(api_key=TAVILY_API_KEY)

# def search_agent(sub_questions: List[str], max_results_per_query: int = 2) -> Dict[str, List[Dict]]:
#     """
#     Search Agent:
#     Fetches top N results for each sub-question.
#     Snippets truncated to 200 chars to speed up Writer.
#     """
#     results = {}
#     for question in sub_questions:
#         try:
#             response = tavily.search(
#                 query=question,
#                 max_results=max_results_per_query,
#                 search_depth="basic",
#                 include_answer=False,
#                 include_raw_content=False,
#                 timeout=5
#             )
#             items = response.get("results", [])
#             # truncate content to 200 chars
#             for item in items:
#                 if "content" in item and item["content"]:
#                     item["content"] = item["content"][:200]
#             results[question] = items
#         except Exception as e:
#             results[question] = [{"error": str(e)}]
#     return results




