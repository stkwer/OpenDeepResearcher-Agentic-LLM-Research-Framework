"""
Pipeline orchestration for OpenDeepResearcher
Connects Planner Agent and Searcher Agent

Milestone 2 (Weeks 3-4):
- Planner breaks down topic into sub-questions
- Searcher gathers raw information for each sub-question
- Returns combined results without summarization
"""

from agents.planner_agent import planner_agent
from agents.searcher_agent import searcher_agent
from typing import Optional, Dict
from datetime import datetime


class ResearchPipeline:
    """
    Orchestrates Planner and Searcher agents for research workflow
    
    Flow:
    1. Planner breaks topic into sub-questions
    2. Searcher gathers raw information for each sub-question
    3. Returns combined results (no summarization)
    """
    
    def __init__(self):
        self.name = "Research Pipeline"
        self.version = "1.0"
    
    def run(self, research_topic: str) -> Optional[Dict]:
        """
        Run research pipeline: plan → search (raw data only)
        
        Args:
            research_topic (str): Main research topic
            
        Returns:
            Dict: Research plan + raw search results
        """
        
        print("\n" + "=" * 70)
        print("🚀 RESEARCH PIPELINE STARTED")
        print("=" * 70)
        
        # Step 1: Create research plan
        print("\n📋 STEP 1: Planning Phase")
        print("-" * 70)
        plan = planner_agent.run(research_topic)
        
        if not plan:
            print("❌ Planning failed!")
            return None
        
        print(f"✅ Plan created with {len(plan['sub_questions'])} sub-questions")
        
        # Step 2: Search for raw information for each sub-question
        print("\n🔍 STEP 2: Information Gathering Phase")
        print("-" * 70)
        search_results = searcher_agent.search_multiple(plan["sub_questions"])
        
        if not search_results:
            print("❌ Search failed!")
            return None
        
        # Step 3: Compile final results (NO summarization)
        print("\n📊 STEP 3: Compilation Phase")
        print("-" * 70)
        
        final_output = {
            "research_topic": research_topic,
            "timestamp": datetime.now().isoformat(),
            "pipeline": {
                "name": self.name,
                "version": self.version
            },
            "planning": plan,
            "search_results": search_results,
            "status": "completed"
        }
        
        print("✅ Research pipeline completed successfully!")
        print(f"✅ Gathered information for {search_results['search_session']['successful_searches']} sub-questions")
        print("=" * 70 + "\n")
        
        return final_output


# Create singleton instance
pipeline = ResearchPipeline()
