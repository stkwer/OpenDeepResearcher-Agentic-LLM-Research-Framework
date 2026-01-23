from langchain_core.messages import HumanMessage
from llm_config import llm
from datetime import datetime
import json, re
from typing import Dict, Optional


class PlannerAgent:
    def __init__(self, num_sub_questions: int = 5):
        self.name = "Planner Agent"
        self.version = "1.0"
        self.num_sub_questions = num_sub_questions

    def run(self, research_topic: str) -> Optional[Dict]:
        """Full autonomous planner pipeline: create → validate → return."""
        print("\nPlanner Agent activated")
        print(f"Analyzing research topic: '{research_topic}'")
        print("Creating research roadmap...\n")

        plan = self._create_initial_plan(research_topic)
        if not plan or not self._validate_plan(plan):
            return None

        # add metadata
        plan["metadata"] = {
            "agent": self.name,
            "version": self.version,
            "created_at": datetime.now().isoformat(),
        }
        return plan

    def _create_initial_plan(self, topic: str) -> Optional[Dict]:
        """Generate initial research plan using LLM."""
        prompt = f"""You are an expert research analyst and strategic planner with deep expertise in breaking down complex topics into actionable research components.

Your task is to decompose the following research topic into {self.num_sub_questions} distinct, logically-ordered sub-questions that form a comprehensive research roadmap.

RESEARCH TOPIC: "{topic}"

CRITICAL REQUIREMENTS:
1. Each sub-question must be specific, measurable, and answerable through research
2. Sub-questions should progress logically from foundational concepts to advanced implications
3. Eliminate any redundancy or overlap between questions
4. Each question should be independent yet collectively form a complete exploration of the topic
5. Use clear, direct language without unnecessary prefixes like "What is" or "How does"
6. Frame questions as research focus areas rather than yes/no questions

STRUCTURE YOUR RESPONSE:
- Start with foundational/definitional sub-questions
- Progress to understanding mechanisms and processes
- Move to analysis and evaluation
- End with applications and implications

OUTPUT FORMAT - Return ONLY valid JSON with NO additional text or explanation:
{{
  "main_question": "{topic}",
  "sub_questions": [
    "Foundational sub-question addressing core concepts",
    "Sub-question exploring key mechanisms or processes",
    "Sub-question analyzing implementation or execution",
    "Sub-question examining challenges or limitations",
    "Sub-question discussing applications or future implications"
  ]
}}

Generate the research roadmap JSON now:"""

        try:
            msg = HumanMessage(content=prompt)
            resp = llm.invoke([msg])
            text = resp.content.strip()
            return self._parse_json(text)
        except Exception as e:
            print(f"Error in LLM call: {e}")
            return None

    def _parse_json(self, text: str) -> Optional[Dict]:
        """Extract and parse JSON from LLM response."""
        try:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                return json.loads(m.group())
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return None

    def _validate_plan(self, plan: Dict) -> bool:
        """Validate that plan has required fields."""
        if "main_question" not in plan or "sub_questions" not in plan:
            return False
        if not isinstance(plan["sub_questions"], list):
            return False
        if len(plan["sub_questions"]) != self.num_sub_questions:
            return False
        return True
    
# singleton instance
planner_agent = PlannerAgent()