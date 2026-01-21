from src.services.tavily_client import TavilyClient


class SearcherAgent:
    def __init__(self):
        self.client = TavilyClient()

    def _clean(self, text: str) -> str:
        if not text:
            return ""

        remove = [
            "subscribe", "likes", "views", "watch", "upgrade",
            "reddit", "youtube", "emoji"
        ]

        text = text.replace("\n", " ")
        for r in remove:
            text = text.replace(r, "")

        return text.strip()

    def _summarize(self, content: str) -> str:
        content = self._clean(content)
        sentences = [s.strip() for s in content.split(".") if len(s.strip()) > 40]
        return ". ".join(sentences[:3]) + "." if sentences else ""

    def run(self, state: dict):
        results = []

        for question in state.get("sub_questions", []):
            data = self.client.search(question)

            sources = []
            for item in data.get("results", []):
                summary = self._summarize(item.get("content", ""))
                if not summary:
                    continue

                sources.append({
                    "summary": summary,
                    "url": item.get("url", ""),
                    "confidence": round(item.get("score", 0.85), 2)
                })

            results.append({
                "question": question,
                "sources": sources
            })

        state["search_results"] = results
        return state









































