class PlannerAgent:
    def run(self, state: dict) -> dict:
        state["outline"] = [
            "Abstract",
            "Introduction",
            "Background",
            "Applications",
            "Trends",
            "Challenges",
            "Future Scope",
            "Conclusion",
            "References"
        ]
        return state
