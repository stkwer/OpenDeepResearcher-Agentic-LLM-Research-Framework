from langchain_ollama import OllamaLLM
from tavily import TavilyClient
import concurrent.futures
from typing import TypedDict, List
import uuid
import time


# ===== LLM SETUP =====
llm = OllamaLLM(model="phi3:mini")


# =====================================================
# ===== PLANNER AGENT =====
# =====================================================
class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, topic: str, num_questions: int = 8):
        prompt = f"""
You are a senior research planning agent for industrial and scientific topics.


Your job:
- Take the user's main topic and decompose it into a structured research roadmap.
- The roadmap consists of deep, non-overlapping sub-questions that together give a rich understanding of the topic.


Design rules:
- Generate exactly {num_questions} sub-questions.
- Start from a high-level overview, then move gradually into more specific and technical issues.
- Cover, where relevant:
  • definitions and basic principles
  • process dynamics and control challenges
  • energy-efficiency aspects
  • safety constraints and operating limits
  • economic or operational trade-offs
  • implementation and tuning issues
  • future research directions
- Each sub-question must be:
  • self-contained (makes sense without the main topic text)
  • precise, not vague
  • focused on something that would require literature review or data analysis to answer
- Do NOT answer the questions.
- Do NOT explain what you are doing.
- Output ONLY the questions as a numbered list from 1 to {num_questions} on separate lines.


Main topic: {topic}
"""
        response = self.llm.invoke(prompt)

        questions = []
        for line in response.splitlines():
            line = line.strip()
            if line:
                # Remove numbering and clean
                question = line.lstrip('0123456789.-•) ')
                if question and len(question) > 10:  # Filter out very short lines
                    questions.append(question[:250])
        
        # Ensure we have at least 4 questions
        if len(questions) < 4:
            questions = [
                f"What are the key principles of {topic}?",
                f"How does {topic} work in practice?",
                f"What are the main applications of {topic}?",
                f"What are the challenges in implementing {topic}?",
                f"What recent developments exist in {topic}?",
                f"How does {topic} compare to similar approaches?",
                f"What are the safety considerations for {topic}?",
                f"What is the future outlook for {topic}?"
            ]
        
        return questions[:num_questions]


# =====================================================
# ===== PARALLEL SEARCHER AGENT =====
# =====================================================
class SearcherAgent:
    def __init__(self, api_key: str, llm):
        self.search_client = TavilyClient(api_key=api_key)
        self.llm = llm
    
    def _search_single_question(self, question: str):
        """Search for a single question"""
        try:
            results = self.search_client.search(
                query=question[:100],
                max_results=1,
                search_depth="basic",
                topic="general",
                include_raw_content=True
            )
            return results.get("results", [])
        except Exception as e:
            print(f"Search error for '{question[:50]}...': {e}")
            return []
    
    def search_and_summarize(self, questions):
        """Search all questions in parallel"""
        if not questions:
            return "No questions provided for research."
        
        # Take only 4-5 questions for faster processing
        search_questions = questions[:5]
        collected_contents = []
        
        # Parallel search with timeout
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_question = {
                    executor.submit(self._search_single_question, q): q
                    for q in search_questions
                }
                
                for future in concurrent.futures.as_completed(future_to_question, timeout=15):
                    try:
                        results = future.result(timeout=5)
                        for result in results:
                            if isinstance(result, dict) and 'content' in result:
                                content = result['content'][:300]
                                collected_contents.append(content)
                    except Exception:
                        continue
        except Exception as e:
            print(f"Parallel search error: {e}")
        
        if not collected_contents:
            return self._generate_fallback_summary(questions[0])
        
        combined_text = " ".join(collected_contents)[:2000]
        return self._summarize_text(combined_text, questions[0])
    
    def _generate_fallback_summary(self, topic: str):
        """Generate summary when search fails"""
        prompt = f"Provide a comprehensive 4-paragraph expert summary about: {topic}"
        return self.llm.invoke(prompt)
    
    def _summarize_text(self, text: str, main_topic: str):
        """Summarize the collected text"""
        prompt = f"""
You are a research synthesis agent. Combine and summarize the following information about {main_topic}:


{text}


Create a coherent 3-paragraph synthesis that:
1. Presents key findings
2. Discusses important aspects
3. Highlights practical implications


Write in academic but clear language.
"""
        return self.llm.invoke(prompt)


# =====================================================
# ===== WRITER AGENT =====
# =====================================================
class WriterAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def write_report(self, topic: str, synthesized_text: str):
        prompt = f"""
You are a professional research writer agent.


Task:
- Convert the given synthesized research paragraph into a structured research report.


Structure:
1. Introduction
2. Core Analysis
3. Practical Implications
4. Challenges and Limitations
5. Future Research Directions
6. Conclusion


Rules:
- Use paragraph format only
- Academic but clear language
- No bullet points
- No URLs or citations
- Do not mention search, sources, or questions
- Make it comprehensive but readable


Topic:
{topic}


Synthesized Research Text:
{synthesized_text}
"""
        return self.llm.invoke(prompt)


# =====================================================
# ===== GLOBAL INITIALIZATION =====
# =====================================================
TAVILY_API_KEY = "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"


planner = PlannerAgent(llm)
searcher = SearcherAgent(TAVILY_API_KEY, llm)
writer = WriterAgent(llm)


# =====================================================
# ===== MAIN RESEARCH FUNCTION =====
# =====================================================
def run_research(topic: str):
    """Main function to run research pipeline"""
    
    # Step 1: Generate research plan (8 questions)
    print(f"📝 Planning research questions for: {topic}")
    questions = planner.create_plan(topic, num_questions=8)
    
    # Step 2: Search and synthesize
    print(f"🔍 Searching for information... ({len(questions)} questions)")
    summary = searcher.search_and_summarize(questions)
    
    # Step 3: Write comprehensive report
    print("✍️ Writing research report...")
    report = writer.write_report(topic, summary)
    
    # IMPORTANT: now also return planner questions to UI
    return {
        "report": report,
        "planner_questions": questions
    }


# =====================================================
# ===== CLI TEST MODE =====
# =====================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 DEEP RESEARCHER - OPTIMIZED VERSION")
    print("=" * 60)
    
    test_topic = "artificial intelligence in healthcare"
    print(f"\nTesting with topic: '{test_topic}'")
    
    start_time = time.time()
    result = run_research(test_topic)
    end_time = time.time()
    
    print(f"\n✅ Research completed in {end_time - start_time:.1f} seconds")
    print("\n" + "=" * 60)
    print("SAMPLE REPORT:")
    print("=" * 60)
    print(result["report"][:500] + "...")
    print("=" * 60)
