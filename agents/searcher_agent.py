from tavily import TavilyClient
from config import SEARCHER_CONFIG
from datetime import datetime
from typing import Dict, List, Optional


class SearcherAgent:
    def __init__(self):
        self.name = "Searcher Agent"
        self.version = "1.0"
        self.api_key = SEARCHER_CONFIG["api_key"]
        self.max_results = SEARCHER_CONFIG["max_results_per_query"]
        
        # Initialize Tavily client
        try:
            self.client = TavilyClient(api_key=self.api_key)
            print("Tavily API connected successfully")
        except Exception as e:
            print(f"Error connecting to Tavily: {e}")
            self.client = None
    
    def search(self, query: str) -> Optional[Dict]:
        """
        Search for information related to a research sub-question
        
        Args:
            query (str): The search query/sub-question
            
        Returns:
            Dict: Raw search results with content and sources (no summarization)
        """
        
        if not self.client:
            print("Tavily client not initialized")
            return None
        
        print(f"Searching: '{query}'")
        
        try:
            # Call Tavily API
            response = self.client.search(
                query=query,
                max_results=self.max_results,
                include_answer=False
            )
            
            # Parse response - keep it raw, no summarization
            search_result = self._parse_search_response(query, response)
            
            if not search_result or not search_result['results']:
                print(f"No results found for: '{query}'")
                return None
            
            print(f"Found {len(search_result['results'])} sources")
            return search_result
            
        except Exception as e:
            print(f"Error during search: {e}")
            return None
    
    def search_multiple(self, sub_questions: List[str]) -> Optional[Dict]:
        """
        Search for multiple sub-questions and compile raw results
        
        Args:
            sub_questions (List[str]): List of sub-questions to search
            
        Returns:
            Dict: Raw search results for all sub-questions
        """
        
        print(f"\nSearching for {len(sub_questions)} sub-questions...")
        
        all_results = {}
        successful_searches = 0
        
        for i, question in enumerate(sub_questions, 1):
            print(f"\n[{i}/{len(sub_questions)}]")
            result = self.search(question)
            
            if result and result['results']:
                all_results[question] = result
                successful_searches += 1
            else:
                all_results[question] = {
                    "query": question,
                    "timestamp": datetime.now().isoformat(),
                    "results": [],
                    "status": "no_results"
                }
        
        # Compile final output
        compiled = {
            "search_session": {
                "agent": self.name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "total_queries": len(sub_questions),
                "successful_searches": successful_searches
            },
            "search_results": all_results
        }
        
        return compiled
    
    def _parse_search_response(self, query: str, response: Dict) -> Dict:
        """
        Parse Tavily search response into structured format (raw, no summarization)
        
        Args:
            query (str): Original search query
            response (Dict): Raw response from Tavily API
            
        Returns:
            Dict: Structured raw search results
        """
        
        parsed = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
        
        # Extract results from API response - keep complete information
        if "results" in response:
            for result in response["results"][:self.max_results]:
                parsed["results"].append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0)
                })
        
        return parsed


# Create singleton instance
searcher_agent = SearcherAgent()
