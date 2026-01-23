"""
Writer Agent for OpenDeepResearcher
Synthesizes search results into coherent summaries using LLM

Milestone 2 (Weeks 3-4):
- Analyzes search results for each sub-question
- Synthesizes information into structured summaries
- Creates comprehensive written responses
"""

from langchain_core.messages import HumanMessage
from llm_config import llm
from datetime import datetime
from typing import Dict, List, Optional
import json


class WriterAgent:
    """
    Writer Agent: Responsible for synthesizing information into written form
    
    Responsibilities:
    1. Analyze search results for each sub-question
    2. Synthesize information into coherent summaries
    3. Organize findings logically
    4. Create structured written responses with limited references
    """
    
    def __init__(self):
        self.name = "Writer Agent"
        self.version = "1.0"
    
    def synthesize(self, sub_question: str, search_results: List[Dict]) -> Optional[Dict]:
        """
        Synthesize search results into a coherent summary
        
        Args:
            sub_question (str): The sub-question being answered
            search_results (List[Dict]): Search results from Searcher Agent
            
        Returns:
            Dict: Synthesized summary with analysis
        """
        
        if not search_results:
            print(f"No search results to synthesize for: '{sub_question}'")
            return None
        
        print(f"\nWriting summary for: '{sub_question}'")
        
        # Prepare content from search results
        search_content = self._prepare_search_content(search_results)
        
        # Create synthesis prompt
        synthesis_prompt = self._create_synthesis_prompt(sub_question, search_content)
        
        # Call LLM to synthesize
        summary = self._synthesize_with_llm(synthesis_prompt)
        
        if not summary:
            print(f"Failed to synthesize summary for: '{sub_question}'")
            return None
        
        # Extract top 2 sources
        top_sources = self._extract_top_sources(search_results, limit=2)
        
        # Compile result with metadata
        result = {
            "sub_question": sub_question,
            "summary": summary,
            "sources": top_sources,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"Summary written ({len(summary.split())} words)")
        return result
    
    def synthesize_multiple(self, planning: Dict, search_results: Dict) -> Optional[Dict]:
        """
        Synthesize search results for all sub-questions into a comprehensive report
        
        Args:
            planning (Dict): Research plan from Planner Agent
            search_results (Dict): Search results from Searcher Agent
            
        Returns:
            Dict: Complete research report with single executive summary
        """
        
        print(f"\nSynthesizing all findings into report structure...\n")
        
        main_question = planning["main_question"]
        sub_questions = planning["sub_questions"]
        search_data = search_results.get("search_results", {})
        
        # Generate SINGLE executive summary based on ALL findings
        print("Generating Executive Summary...")
        
        # Collect all search content first
        all_search_content = {}
        for sub_question in sub_questions:
            results = search_data.get(sub_question, {}).get("results", [])
            all_search_content[sub_question] = self._prepare_search_content(results)
        
        executive_summary = self._generate_comprehensive_executive_summary(
            main_question, 
            sub_questions, 
            all_search_content
        )
        
        # Synthesize each section
        sections = {}
        all_sources = set()
        
        for i, sub_question in enumerate(sub_questions, 1):
            print(f"Writing Section {i}/{len(sub_questions)}")
            
            # Get search results for this sub-question
            results = search_data.get(sub_question, {}).get("results", [])
            
            # Synthesize into section
            synthesis = self.synthesize(sub_question, results)
            
            if synthesis:
                section_key = f"section_{i}"
                sections[section_key] = {
                    "sub_question": sub_question,
                    "content": synthesis["summary"],
                    "sources": synthesis["sources"]  # Only top 2 sources
                }
                
                # Collect all unique sources from top sources only
                all_sources.update([s["url"] for s in synthesis["sources"]])
        
        # Generate conclusion
        print("Generating Conclusion...")
        conclusion = self._generate_conclusion(main_question, sections)
        
        # Compile complete report with limited references
        report = {
            "main_topic": main_question,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": executive_summary,
            "sections": sections,
            "conclusion": conclusion,
            "references": self._get_unique_sources(list(all_sources)),  # Limited references
            "total_sections": len(sections),
            "total_references": len(list(all_sources))
        }
        
        print(f"\nReport synthesis complete!")
        print(f"Total References: {report['total_references']}")
        return report
    
    def _prepare_search_content(self, search_results: List[Dict]) -> str:
        """
        Prepare search results into readable text for LLM
        
        Args:
            search_results (List[Dict]): Search results
            
        Returns:
            str: Formatted sources text
        """
        
        content_parts = []
        
        for i, result in enumerate(search_results, 1):
            content_parts.append(f"Source {i}: {result.get('title', 'N/A')}")
            content_parts.append(f"URL: {result.get('url', 'N/A')}")
            content_parts.append(f"Content: {result.get('content', 'No content')}")
            content_parts.append("-" * 80)
        
        return "\n".join(content_parts)
    
    def _create_synthesis_prompt(self, sub_question: str, search_content: str) -> str:
        """
        Create prompt for LLM to synthesize information
        
        Args:
            sub_question (str): Sub-question to answer
            search_content (str): Formatted sources content
            
        Returns:
            str: Synthesis prompt
        """
        
        prompt = f"""You are a professional research writer tasked with synthesizing information into clear, coherent summaries.


RESEARCH SUB-QUESTION: "{sub_question}"


SEARCH RESULTS TO SYNTHESIZE:
{search_content}


TASK:
1. Read through all the search results above
2. Extract the most relevant and important information
3. Synthesize this information into a clear, well-structured summary
4. Focus on answering the research sub-question
5. Write in professional, academic language
6. Aim for 200-300 words
7. Do NOT include citations in the text (we'll track sources separately)
8. Do NOT mention "according to source X" or similar phrases
9. Present the information as synthesized knowledge


Write the summary now:"""
        
        return prompt
    
    def _synthesize_with_llm(self, prompt: str) -> Optional[str]:
        """
        Call LLM to synthesize information
        
        Args:
            prompt (str): Synthesis prompt
            
        Returns:
            Optional[str]: Synthesized text or None
        """
        
        try:
            msg = HumanMessage(content=prompt)
            resp = llm.invoke([msg])
            summary = resp.content.strip()
            return summary
        except Exception as e:
            print(f"Error in LLM synthesis: {e}")
            return None
    
    def _extract_top_sources(self, search_results: List[Dict], limit: int = 2) -> List[Dict]:
        """
        Extract top N sources by score/relevance
        
        Args:
            search_results (List[Dict]): All search results
            limit (int): Number of sources to extract
            
        Returns:
            List[Dict]: Top N sources
        """
        
        sources = []
        
        # Take top N results (already ranked by Tavily)
        for result in search_results[:limit]:
            sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", "")
            })
        
        return sources
    
    def _get_unique_sources(self, all_urls: List[str]) -> List[Dict]:
        """
        Get unique sources and format them
        
        Args:
            all_urls (List[str]): All source URLs
            
        Returns:
            List[Dict]: Unique formatted sources (limited to top sources)
        """
        
        unique_urls = list(set(all_urls))
        
        sources = []
        for idx, url in enumerate(unique_urls, 1):
            # Extract title from URL if possible, otherwise use generic title
            title = url.split('/')[-1] or url.split('//')[1].split('/')[0]
            
            sources.append({
                "number": idx,
                "title": title,
                "url": url
            })
        
        return sources
    
    def _generate_comprehensive_executive_summary(
        self, 
        main_topic: str, 
        sub_questions: List[str], 
        all_search_content: Dict[str, str]
    ) -> str:
        """
        Generate a SINGLE comprehensive executive summary based on all findings
        
        Args:
            main_topic (str): Main research topic
            sub_questions (List[str]): All sub-questions
            all_search_content (Dict): Search content for each sub-question
            
        Returns:
            str: Comprehensive executive summary
        """
        
        # Create detailed content for prompt
        content_preview = ""
        for question, content in list(all_search_content.items())[:3]:  # First 3 for context
            content_preview += f"\n{question}:\n{content[:500]}...\n"
        
        prompt = f"""You are an expert research analyst and professional writer.


MAIN RESEARCH TOPIC: "{main_topic}"


KEY RESEARCH AREAS:
{chr(10).join([f"{i}. {q}" for i, q in enumerate(sub_questions, 1)])}


RESEARCH CONTENT OVERVIEW:
{content_preview}


TASK:
Generate a comprehensive executive summary (300-400 words) that:
1. Provides a complete overview of the research topic
2. Highlights key findings across all research areas
3. Explains the significance and relevance of the findings
4. Synthesizes major themes and insights
5. Sets context for detailed sections
6. Uses professional, academic language
7. Does NOT include citations or reference URLs


Write the executive summary now:"""
        
        try:
            msg = HumanMessage(content=prompt)
            resp = llm.invoke([msg])
            return resp.content.strip()
        except Exception as e:
            print(f"Error generating executive summary: {e}")
            return "Executive summary generation failed."
    
    def _generate_conclusion(self, main_topic: str, sections: Dict) -> str:
        """
        Generate conclusion synthesizing all findings
        
        Args:
            main_topic (str): Main research topic
            sections (Dict): All report sections
            
        Returns:
            str: Conclusion text
        """
        
        section_summaries = "\n".join([
            f"• {s['sub_question']}"
            for s in sections.values()
        ])
        
        prompt = f"""You are a professional research writer.


MAIN RESEARCH TOPIC: "{main_topic}"


SECTIONS COVERED:
{section_summaries}


Generate a conclusion (200-250 words) that:
1. Synthesizes the key findings from all sections
2. Explains how the findings answer the main research question
3. Discusses implications and significance
4. Suggests future research directions
5. Does NOT include citations
6. Uses professional, academic language


Write the conclusion now:"""
        
        try:
            msg = HumanMessage(content=prompt)
            resp = llm.invoke([msg])
            return resp.content.strip()
        except Exception as e:
            print(f"Error generating conclusion: {e}")
            return "Conclusion generation failed."


# Create singleton instance
writer_agent = WriterAgent()
