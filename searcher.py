import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.search_client import search_web


class SearcherAgent:
    """
    Performs web research safely.
    """

    def search(self, sub_question: str) -> list:
        try:
            results = search_web(sub_question)
            if not isinstance(results, list):
                return []
            return results[:3]
        except Exception as e:
            print(f"⚠ Search failed: {e}")
            return []
