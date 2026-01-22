class ResearchAssistant:
    def __init__(self):
        self.name = "Agentic Research Assistant"

    def assist(self, query):
        return f"Research insights generated for: {query}"


if __name__ == "__main__":
    assistant = ResearchAssistant()
    print(assistant.assist("Explain Agentic LLM frameworks"))
  
