from dotenv import load_dotenv
import os

from agents.planner_agent import PlannerAgent
from agents.searcher_agent import SearcherAgent
from agents.writer_agent import WriterAgent

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

def main():
    topic = input("Enter topic: ")

    planner = PlannerAgent(GEMINI_KEY)
    searcher = SearcherAgent(TAVILY_KEY)
    writer = WriterAgent(GEMINI_KEY)

    questions = planner.run(topic)
    research_log = searcher.run(questions)
    output = writer.run(topic, research_log)

    print("\nFINAL OUTPUT:\n")
    print(output)

if __name__ == "__main__":
    main()
