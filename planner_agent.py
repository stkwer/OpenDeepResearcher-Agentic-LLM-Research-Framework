"""
planner_agent.py

Planner Agent - Uses LM Studio to split user questions into unique subquestions.
Calls the running LM Studio server to generate intelligent subquestions for each input.
"""

import json
import re
import uuid
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional


class PlannerAgent:
    """
    Planner Agent that uses LM Studio to generate unique subquestions
    for each user query. Connects to the running LM Studio server.
    """

    def __init__(self):
        self.api_url = "http://127.0.0.1:1234/v1/chat/completions"
        self.model_name = "local-model"
        self.question_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat() + "Z"

    def _build_system_prompt(self) -> str:
        """Kept for backward compatibility but not used in agent-based mode."""
        return "Agent-based planner: no system prompt needed."

    def _call_lm_studio(self, messages: List[Dict[str, str]]) -> str:
        """
        Call LM Studio server and return the response text.
        """
        try:
            # messages: list of {role,content}
            payload = {
                "model": self.model_name,
                "messages": messages,
                # allow caller to embed temperature/max_tokens in messages if needed
                "temperature": 0.3,
                "max_tokens": 1024,
            }
            print("[planner] Sending request to LM Studio (may take a moment)...")
            response = requests.post(self.api_url, json=payload, timeout=180)

            if response.status_code != 200:
                print(f"[planner] LM Studio error: {response.status_code}: {response.text[:200]}")
                return ""

            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.Timeout:
            print("[planner] Warning: LM Studio took too long to respond. The model may be slow.")
            print("[planner] Try again or check if the server is overloaded.")
            return ""
        except requests.exceptions.ConnectionError:
            print("[planner] Error: Cannot connect to LM Studio on port 1234. Make sure the server is running.")
            return ""
        except Exception as e:
            print(f"[planner] Error calling LM Studio: {e}")
            return ""

    def _generate_subquestions_lm(self, user_prompt: str) -> List[Dict[str, Any]]:
        """
        Use LM Studio to intelligently break down the user's question into subquestions.
        Returns all subquestions in ONE call (no retries).
        """
        # Strong instruction with a concrete example to encourage correct JSON output
        system_prompt = (
            "You are a research planning expert. Your single task is to break a research question into EXACTLY 6-8 "
            "atomic, focused subquestions. Each subquestion must be answerable and non-overlapping. "
            "Return ONLY a JSON array (no markdown, no explanation). Each item must be an object: "
            "{\"id\": \"q1\", \"text\": \"...\", \"priority\": 1, \"type\": \"analysis\"} . "
            "Types allowed: background, definition, analysis, methodology, causal, impact, comparative, historical. "
            "Prioritize by importance (1 = highest). Keep each subquestion concise (<=140 chars). "
            "IMPORTANT: You MUST generate exactly 6-8 subquestions, not 1-2."
        )

        # Provide a generic example without specific content
        example = (
            "EXAMPLE:\nUser prompt: \"What are the main impacts of artificial intelligence?\"\n"
            "Output JSON:\n"
            "[\n  {\"id\": \"q1\", \"text\": \"What are the main types of AI technologies?\", \"priority\": 1, \"type\": \"background\"},\n"
            "  {\"id\": \"q2\", \"text\": \"How do AI systems process information?\", \"priority\": 2, \"type\": \"methodology\"},\n"
            "  {\"id\": \"q3\", \"text\": \"What are the economic impacts of AI adoption?\", \"priority\": 3, \"type\": \"impact\"},\n"
            "  {\"id\": \"q4\", \"text\": \"What are the ethical challenges of AI implementation?\", \"priority\": 4, \"type\": \"analysis\"},\n"
            "  {\"id\": \"q5\", \"text\": \"How does AI compare to traditional computing methods?\", \"priority\": 5, \"type\": \"comparative\"},\n"
            "  {\"id\": \"q6\", \"text\": \"What are the future trends in AI development?\", \"priority\": 6, \"type\": \"historical\"}\n]"
        )

        user_message = (
            f"Produce EXACTLY 6-8 focused subquestions for the research question below. Output ONLY the JSON array with all subquestions.\n\n"
            f"Research question:\n{user_prompt}\n\nPlease ensure items are concise, non-overlapping, and answerable. You must generate 6-8 subquestions."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": example + "\n\n" + user_message}
        ]

        response_text = self._call_lm_studio(messages)

        if not response_text:
            print("[planner] LM Studio returned empty response.")
            # Generate multiple fallback subquestions instead of just one
            return [
                {"id": "q1", "text": f"What is the background of {user_prompt}?", "priority": 1, "type": "background"},
                {"id": "q2", "text": f"How does {user_prompt} work?", "priority": 2, "type": "methodology"},
                {"id": "q3", "text": f"What are the impacts of {user_prompt}?", "priority": 3, "type": "impact"},
                {"id": "q4", "text": f"What are the challenges with {user_prompt}?", "priority": 4, "type": "analysis"},
                {"id": "q5", "text": f"How does {user_prompt} compare to alternatives?", "priority": 5, "type": "comparative"},
                {"id": "q6", "text": f"What are the future trends for {user_prompt}?", "priority": 6, "type": "historical"}
            ]

        # Try to parse JSON from response
        parsed = None
        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError:
            # try to extract JSON array
            m = re.search(r"\[.*\]", response_text, re.DOTALL)
            if m:
                try:
                    parsed = json.loads(m.group(0))
                except json.JSONDecodeError:
                    parsed = None

        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        
        # Fallback: return multiple subquestions if parsing fails
        print(f"[planner] Could not parse JSON from LM Studio. Raw output:\n{response_text[:500]}")
        return [
            {"id": "q1", "text": f"What is the background of {user_prompt}?", "priority": 1, "type": "background"},
            {"id": "q2", "text": f"How does {user_prompt} work?", "priority": 2, "type": "methodology"},
            {"id": "q3", "text": f"What are the impacts of {user_prompt}?", "priority": 3, "type": "impact"},
            {"id": "q4", "text": f"What are the challenges with {user_prompt}?", "priority": 4, "type": "analysis"},
            {"id": "q5", "text": f"How does {user_prompt} compare to alternatives?", "priority": 5, "type": "comparative"},
            {"id": "q6", "text": f"What are the future trends for {user_prompt}?", "priority": 6, "type": "historical"}
        ]

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'what', 'which',
            'who', 'when', 'where', 'why', 'how', 'this', 'that', 'these', 'those'
        }
        
        # Extract words (remove punctuation)
        words = re.findall(r'\b[a-z]+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return list(set(keywords))[:10]  # Return unique keywords, max 10

    @staticmethod
    def detect_question_type(text: str) -> str:
        """Detect the type of research question."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['how', 'method', 'process', 'way']):
            return 'methodology'
        elif any(word in text_lower for word in ['why', 'cause', 'reason', 'effect']):
            return 'causal'
        elif any(word in text_lower for word in ['what', 'definition', 'mean', 'is']):
            return 'definition'
        elif any(word in text_lower for word in ['compare', 'difference', 'versus', 'vs']):
            return 'comparative'
        elif any(word in text_lower for word in ['trend', 'history', 'evolution', 'over time']):
            return 'historical'
        elif any(word in text_lower for word in ['impact', 'effect', 'consequence', 'result']):
            return 'impact'
        else:
            return 'analysis'

    @staticmethod
    def split_into_subquestions(user_prompt: str) -> List[Dict[str, Any]]:
        """
        Delegates to LM Studio for intelligent subquestion generation.
        """
        agent = PlannerAgent()
        return agent._generate_subquestions_lm(user_prompt)

    @staticmethod
    def create_research_plan(subquestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a structured research plan based on subquestions.
        """
        plan = []
        step = 1

        # Search step for each subquestion
        for subq in subquestions:
            search_target = ["web", "academic"]
            if subq["type"] in ["historical", "trend"]:
                search_target.append("archive")
            
            plan.append({
                "step": step,
                "action": "search",
                "target": search_target,
                "query_template": f"{subq['text']} -wiki",
                "expected_results": 5,
                "depends_on": [subq["id"]]
            })
            step += 1

        # Synthesis step
        subq_ids = [sq["id"] for sq in subquestions]
        plan.append({
            "step": step,
            "action": "synthesize",
            "depends_on": subq_ids,
            "method": "cross-reference analysis"
        })
        step += 1

        # Validation step
        plan.append({
            "step": step,
            "action": "validate",
            "depends_on": ["synthesis"],
            "method": "fact-check against multiple sources"
        })

        return plan

    @staticmethod
    def extract_constraints(user_prompt: str) -> Dict[str, Any]:
        """
        Extract constraints from the user prompt.
        """
        constraints = {
            "time_horizon": None,
            "source_types": ["peer-reviewed", "official", "news"],
            "domain_focus": None
        }

        # Check for date ranges
        date_pattern = r'(\d{4})\s*(?:to|-|–)\s*(\d{4})'
        date_match = re.search(date_pattern, user_prompt)
        if date_match:
            constraints["time_horizon"] = f"{date_match.group(1)}-01-01 to {date_match.group(2)}-12-31"

        # Check for specific source preferences
        if any(word in user_prompt.lower() for word in ['scholarly', 'academic', 'peer-reviewed']):
            constraints["source_types"] = ["peer-reviewed"]
        elif any(word in user_prompt.lower() for word in ['news', 'recent']):
            constraints["source_types"] = ["news", "official"]

        # Extract domain focus
        keywords = PlannerAgent.extract_keywords(user_prompt)
        if keywords:
            constraints["domain_focus"] = keywords[0]

        return constraints

    def plan(self, user_prompt: str) -> Dict[str, Any]:
        """
        Generate a planner JSON using LM Studio to generate intelligent subquestions.
        
        Returns the parsed planner JSON (and writes it to file).
        """
        print(f"\n[planner] Processing question: {user_prompt[:100]}...")
        print("[planner] Calling LM Studio to generate subquestions...")

        # Generate unique subquestions using LM Studio
        subquestions = self._generate_subquestions_lm(user_prompt)
        print(f"\n[planner] Generated {len(subquestions)} subquestions:")
        print("-" * 70)
        
        for sq in subquestions:
            priority = sq.get("priority", "?")
            q_type = sq.get("type", "?")
            text = sq.get("text", "")
            print(f"  [{sq['id']} - Priority {priority} - {q_type}] {text}")
        
        print("-" * 70)

        # Create research plan
        plan = self.create_research_plan(subquestions)
        print(f"[planner] Created research plan with {len(plan)} steps")

        # Extract constraints
        constraints = self.extract_constraints(user_prompt)
        print("[planner] Extracted constraints from prompt")

        # Build the final JSON output
        result = {
            "question_id": self.question_id,
            "original_prompt": user_prompt,
            "summary": user_prompt.split('.')[0] + "." if '.' in user_prompt else user_prompt,
            "subquestions": subquestions,
            "plan": plan,
            "constraints": constraints,
            "metadata": {
                "planner_version": "v2-lm-studio",
                "created_at": self.created_at,
                "method": "LM Studio inference"
            }
        }

        # Save to disk
        filename = f"planner_output_{self.question_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[planner] Saved planner output to: {filename}\n")

        return result


if __name__ == "__main__":
    agent = PlannerAgent()

    print("=" * 70)
    print("Planner Agent (Using LM Studio Server)")
    print("Generates intelligent subquestions using the loaded model.")
    print("=" * 70)
    print("Make sure LM Studio is running with port 1234 active!")
    print("=" * 70)

    try:
        while True:
            q = input("\nEnter your research question → ").strip()
            if not q:
                continue
            if q.lower() in ("exit", "quit"):
                print("Exiting.")
                break
            try:
                result = agent.plan(q)
            except Exception as e:
                print(f"[planner] Error: {e}")
                import traceback
                traceback.print_exc()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye.")
