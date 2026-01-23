import requests
import json
from typing import List, Dict, Any
from planner_agent import PlannerAgent
from searcher_agent import SearcherAgent

class WriterAgent:
    """
    Writer Agent: Synthesizes retrieved data from searcher into structured, coherent summaries using LM Studio.
    """

    def __init__(self):
        self.api_url = "http://127.0.0.1:1234/v1/chat/completions"
        self.model_name = "local-model"

    def _call_lm_studio(self, messages: List[Dict[str, str]]) -> str:
        """
        Call LM Studio to generate synthesis report - LM Studio output only.
        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 3072,  # Increased for full-page content
            "stream": False
        }

        # LM Studio only - no fallbacks
        timeout = 600  # Back to 10 minutes with optimized settings
        print(f"[writer] Generating report with LM Studio (timeout: {timeout}s)...")
        
        # Use raw connection for better control
        response_text = ""
        try:
            response = requests.post(
                self.api_url, 
                json=payload, 
                timeout=timeout,
                headers={'Connection': 'close'}  # Force connection close
            )
            
            # Get raw response text
            response_text = response.text
            print(f"[writer] LM Studio response received! Length: {len(response_text)} chars")
            
            # Parse JSON manually
            try:
                data = json.loads(response_text)
                if "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
                    content = data["choices"][0]["message"]["content"]
                    print(f"[writer] Report generation completed successfully!")
                    return content
                else:
                    print(f"[writer] Invalid response structure: missing 'choices' or 'message' field")
                    print(f"[writer] Response data: {str(data)[:500]}...")
                    return f"LM Studio returned invalid response structure. Missing 'choices' or 'message' field."
            except (KeyError, IndexError, TypeError) as struct_error:
                print(f"[writer] Response structure error: {struct_error}")
                print(f"[writer] Response data: {response_text[:500]}...")
                return f"LM Studio response structure error: {str(struct_error)}"
            
        except json.JSONDecodeError as e:
            print(f"[writer] JSON decode error: {e}")
            print(f"[writer] Raw response: {response_text[:500]}...")
            # Try to extract content from partial JSON
            if response_text and '"content"' in response_text:
                try:
                    import re
                    content_match = re.search(r'"content":\s*"([^"]*(?:\\.[^"]*)*)"', response_text)
                    if content_match:
                        content = content_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                        print(f"[writer] Extracted content from partial JSON")
                        return content
                except Exception as extract_error:
                    print(f"[writer] Content extraction failed: {extract_error}")
            return f"LM Studio response error: {str(e)}"
        except requests.exceptions.ReadTimeout as e:
            print(f"[writer] Read timeout occurred but content may be available: {e}")
            # Try to extract partial content if available
            if response_text:
                print(f"[writer] Attempting to extract content from {len(response_text)} characters of response...")
                print(f"[writer] Response preview: {response_text[:200]}...")
                
                try:
                    # Try to parse as JSON first
                    data = json.loads(response_text)
                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0]["message"]["content"]
                        print(f"[writer] Successfully extracted content from timeout response! Length: {len(content)} characters")
                        return content
                except json.JSONDecodeError as je:
                    print(f"[writer] JSON parsing failed: {je}")
                    # If JSON parsing fails, try multiple extraction methods
                    content_extracted = None
                    
                    # Method 1: Try to find content field with regex
                    try:
                        import re
                        # More robust regex that handles escaped quotes and newlines
                        content_patterns = [
                            r'"content":\s*"((?:[^"\\]|\\.)*)"',  # Basic pattern
                            r'"content":\s*"([^"]*(?:\\.[^"]*)*)"',  # Extended pattern
                            r'"content":\s*"(.+?)"(?=\s*,|\s*})',  # Until next comma or brace
                        ]
                        
                        for pattern in content_patterns:
                            content_match = re.search(pattern, response_text, re.DOTALL)
                            if content_match:
                                content = content_match.group(1)
                                content = content.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
                                if len(content) > 100:  # Only accept if substantial
                                    content_extracted = content
                                    print(f"[writer] Extracted content using regex pattern! Length: {len(content)} characters")
                                    break
                    except Exception as regex_error:
                        print(f"[writer] Regex extraction failed: {regex_error}")
                    
                    # Method 2: Try to extract from the actual response structure
                    if not content_extracted:
                        try:
                            # Look for the actual content between assistant tags
                            assistant_match = re.search(r'<\|im_start\|>assistant\n(.*?)<\|im_end\|>', response_text, re.DOTALL)
                            if assistant_match:
                                content = assistant_match.group(1).strip()
                                if len(content) > 100:
                                    content_extracted = content
                                    print(f"[writer] Extracted content from assistant tags! Length: {len(content)} characters")
                        except Exception as tag_error:
                            print(f"[writer] Tag extraction failed: {tag_error}")
                    
                    # Method 3: Last resort - extract everything after the last assistant tag
                    if not content_extracted:
                        try:
                            last_assistant_pos = response_text.rfind('assistant\n')
                            if last_assistant_pos != -1:
                                content = response_text[last_assistant_pos + 21:].strip()
                                # Remove any trailing </|im_end|> tags
                                content = re.sub(r'<\|im_end\|>.*$', '', content, flags=re.DOTALL)
                                if len(content) > 100:
                                    content_extracted = content
                                    print(f"[writer] Extracted content using fallback method! Length: {len(content)} characters")
                        except Exception as fallback_error:
                            print(f"[writer] Fallback extraction failed: {fallback_error}")
                    
                    # Method 4: Try to extract any text that looks like a report
                    if not content_extracted:
                        try:
                            # Look for text that starts with a capital letter and contains multiple sentences
                            text_patterns = [
                                r'([A-Z][^.!?]*[.!?](?:\s+[A-Z][^.!?]*[.!?]){2,})',  # Multiple sentences
                                r'([A-Z][^.!?]*[.!?]\s+[A-Z][^.!?]*[.!?])',  # At least 2 sentences
                            ]
                            
                            for pattern in text_patterns:
                                text_match = re.search(pattern, response_text, re.DOTALL)
                                if text_match:
                                    content = text_match.group(1).strip()
                                    if len(content) > 200:  # Substantial content
                                        content_extracted = content
                                        print(f"[writer] Extracted content using text pattern! Length: {len(content)} characters")
                                        break
                        except Exception as text_error:
                            print(f"[writer] Text pattern extraction failed: {text_error}")
                    
                    if content_extracted:
                        print(f"[writer] Successfully extracted LM Studio generated content despite timeout!")
                        return content_extracted
                    else:
                        print(f"[writer] Could not extract substantial content from timeout response")
                        print(f"[writer] Full response preview: {response_text[:1000]}...")
                        
            # If we can't extract content, provide a helpful message
            return f"LM Studio timeout after {timeout}s, but content was generated. Please try again or check LM Studio logs for the complete response."
        except Exception as e:
            print(f"[writer] LM Studio connection error: {e}")
            return f"LM Studio connection error: {str(e)}"

    def _generate_fallback_report(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a basic structured report as fallback.
        """
        try:
            # Extract research question from user message
            research_question = "Unknown Research Topic"
            for message in messages:
                if message["role"] == "user":
                    lines = message["content"].split("\n")
                    for line in lines:
                        if "Research Question:" in line:
                            research_question = line.split("Research Question:")[1].strip()
                            break
                    break
            
            # Create a structured 5-paragraph fallback report
            report = f"""The field of {research_question.lower()} represents a significant area of contemporary research and practice. This comprehensive analysis examines the fundamental aspects and implications of the subject matter, drawing upon available scholarly sources and empirical evidence. The importance of understanding this topic has grown substantially in recent years, reflecting its relevance to both theoretical frameworks and practical applications. Researchers and practitioners alike recognize the need for thorough investigation into the various dimensions and complexities that characterize this domain. Such inquiry provides valuable insights that can inform future developments and strategic decision-making processes across multiple contexts.

Current research indicates that {research_question.lower()} has evolved through several distinct phases of development and refinement. Existing literature demonstrates a progression from early theoretical foundations to more sophisticated contemporary approaches that integrate advanced methodologies and technologies. The historical context reveals how various factors have influenced the trajectory of research in this area, including technological advancements, changing societal needs, and evolving theoretical paradigms. This evolutionary process has resulted in a rich tapestry of knowledge that continues to expand and diversify as new discoveries emerge. Understanding this developmental trajectory is essential for contextualizing current research efforts and identifying promising directions for future investigation.

The analysis of available sources reveals several key findings that highlight the multifaceted nature of {research_question.lower()}. Research evidence consistently demonstrates the interconnected relationships between various components and subsystems within this domain, suggesting the need for holistic approaches to understanding and implementation. Empirical studies have identified critical success factors and potential challenges that must be addressed to achieve optimal outcomes in practice. Furthermore, the integration of theoretical frameworks with practical applications has yielded valuable insights into effective strategies and methodologies. These findings collectively contribute to a more nuanced understanding of the subject matter and provide a foundation for evidence-based decision-making.

The practical implications of {research_question.lower()} extend across numerous sectors and applications, making it a critical area of focus for policymakers, practitioners, and researchers. Implementation challenges and opportunities vary significantly depending on contextual factors, including organizational structures, resource availability, and stakeholder engagement. The potential benefits of successful application include improved efficiency, enhanced effectiveness, and sustainable outcomes that align with broader strategic objectives. However, realizing these benefits requires careful consideration of various constraints and limitations that may impact implementation processes. Stakeholders must therefore adopt strategic approaches that balance innovation with practical considerations to maximize positive outcomes while minimizing potential risks and challenges.

Future research directions in {research_question.lower()} should focus on addressing current knowledge gaps and exploring emerging opportunities for advancement. Interdisciplinary collaboration and methodological innovation will be essential for advancing understanding and developing more sophisticated approaches to complex challenges. The integration of emerging technologies and novel theoretical frameworks offers promising avenues for future investigation and application. Additionally, increased emphasis on longitudinal studies and cross-cultural comparisons can provide valuable insights into the generalizability and transferability of findings across different contexts. Such continued research efforts will contribute to the ongoing evolution of the field and support the development of more effective and sustainable solutions.

Note: This is a fallback report generated due to technical difficulties with the AI service. Please try again for a comprehensive analysis with current research data and citations."""
            return report
        except Exception as e:
            print(f"[writer] Fallback generation error: {e}")
            return f"Error generating report. Please try again. Technical details: {str(e)}"

    def _generate_immediate_fallback(self, research_question: str, subquestions: List[Dict[str, Any]]) -> str:
        """
        Generate an immediate fallback report when search results are empty.
        """
        try:
            # Create a structured 5-paragraph immediate fallback report
            report = f"""The investigation into {research_question.lower()} represents an important scholarly endeavor that seeks to advance understanding in this significant area of study. This comprehensive analysis aims to explore the fundamental dimensions and implications of the subject matter through systematic examination of available evidence and theoretical frameworks. The relevance of this research has become increasingly apparent in contemporary academic and professional contexts, reflecting growing recognition of its importance across multiple domains of practice. Scholars and practitioners continue to emphasize the critical need for thorough investigation into the various aspects and complexities that characterize this field. Such systematic inquiry provides essential insights that can inform theoretical development and practical applications in meaningful ways.

The current state of knowledge regarding {research_question.lower()} reveals a complex landscape of theoretical perspectives and empirical findings that have evolved over time. Contemporary literature demonstrates significant progress in understanding the underlying mechanisms and principles that govern phenomena within this domain of study. Historical developments have laid important groundwork for current research efforts, establishing foundational concepts and methodological approaches that continue to inform scholarly investigation. The evolution of thought in this area reflects broader trends in academic research, including increased emphasis on interdisciplinary collaboration and methodological sophistication. Understanding this historical and theoretical context is crucial for situating current research within the broader scholarly conversation and identifying promising directions for future investigation.

Analysis of the subject matter reveals several critical insights that contribute to a more nuanced understanding of {research_question.lower()}. Theoretical frameworks provide valuable lenses through which to examine complex phenomena and identify patterns that might otherwise remain obscured. Empirical evidence, while limited in this case, suggests important relationships between various factors and outcomes that warrant further investigation. Methodological approaches employed in studying this topic have become increasingly sophisticated, incorporating advanced analytical techniques and innovative research designs. These developments collectively enhance our capacity to generate meaningful insights and advance knowledge in ways that can inform both theory and practice across multiple contexts.

The practical implications of research in {research_question.lower()} extend far beyond academic considerations, influencing policy development, professional practice, and organizational decision-making processes. Implementation of research findings requires careful attention to contextual factors that may affect the transferability and applicability of theoretical insights to real-world situations. Stakeholders across various sectors must consider the potential benefits and challenges associated with applying knowledge generated through scholarly investigation. The integration of research evidence into practice demands strategic approaches that balance theoretical rigor with practical considerations and resource constraints. Such thoughtful application of scholarly knowledge can lead to improved outcomes and more effective approaches to addressing complex challenges in diverse settings.

Future research directions in {research_question.lower()} should prioritize addressing current knowledge gaps while exploring innovative approaches to longstanding questions and challenges. Interdisciplinary collaboration offers promising opportunities to generate novel insights through the integration of diverse perspectives and methodological approaches. Technological advancements and emerging analytical tools provide new capabilities for investigating complex phenomena and generating sophisticated analyses that were previously impossible. Longitudinal studies and cross-cultural investigations can provide valuable insights into the generalizability and transferability of findings across different contexts and populations. Such continued research efforts will contribute to the ongoing advancement of knowledge and support the development of more effective and sustainable solutions to complex problems.

Note: This is an immediate fallback report generated due to empty search results. Please try again with different subquestions or search parameters for a comprehensive analysis with current research data and citations."""
            return report
        except Exception as e:
            print(f"[writer] Immediate fallback generation error: {e}")
            return f"Error generating report. Please try again. Technical details: {str(e)}"

    def synthesize_report(self, research_question: str, subquestions: List[Dict[str, Any]], search_results: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Synthesize a comprehensive, well-written passage-style report from subquestions and search results.
        Creates a cohesive narrative instead of question-answer format.
        Enhanced with citations and substantial paragraph generation.
        """
        # Immediate fallback if no search results or LM Studio issues
        if not search_results or not any(search_results.values()):
            return self._generate_immediate_fallback(research_question, subquestions)
        
        # Build enhanced context with limited sources to avoid context overflow
        context = []
        citations = {}
        
        for qid, sources in search_results.items():
            subq_text = next((sq["text"] for sq in subquestions if sq.get("id") == qid), qid)
            if sources:
                # Take only top 2 sources per subquestion to reduce context size
                for i, source in enumerate(sources[:2], 1):
                    # Create citation key
                    citation_key = f"[{qid.upper()}{i}]"
                    citations[citation_key] = {
                        'title': source['title'],
                        'url': source['url']
                    }
                    
                    # Limit content to 200 characters to further reduce context
                    content = source['content'][:200] + "..." if len(source['content']) > 200 else source['content']
                    
                    context.append({
                        'topic': subq_text,
                        'title': source['title'],
                        'content': content,
                        'citation': citation_key
                    })
        
        # Create comprehensive context string with citations
        context_str = "\n\n".join([
            f"Topic: {item['topic']}\nSource: {item['title']}\nContent: {item['content']}\nCitation: {item['citation']}"
            for item in context
        ])

        # Enhanced system prompt for detailed, professional paragraphs with citations
        system_prompt = (
            "You are an expert research writer. Write a comprehensive 8-paragraph academic report. "
            "Each paragraph: 5-7 sentences, 120-180 words for balanced content. "
            "Structure: 1) Introduction, 2) Background, 3) Literature Review, 4) Methodology/Approach, "
            "5) Analysis with citations, 6) Implications, 7) Challenges/Limitations, 8) Conclusion. "
            "Use formal academic tone, complex sentences, and in-text citations [CITATION]. "
            "No headings or Q&A format - create flowing narrative. Provide detailed analysis and examples."
        )

        user_prompt = f"""
Research Question: {research_question}

Research Materials with Citations:
{context_str}

Write a comprehensive 8-paragraph academic report:
1. Introduction (topic significance, context, importance)
2. Background (current state, historical development, key concepts)
3. Literature Review (existing research, scholarly perspectives)
4. Methodology/Approach (analytical framework, research methods)
5. Analysis (findings with citations, evidence, detailed examination)
6. Implications (practical impact, applications, consequences)
7. Challenges/Limitations (constraints, future research needs)
8. Conclusion (summary, recommendations, future directions)

Each paragraph: 5-7 sentences, 120-180 words, include citations [CITATION], no instructions in response."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        print("[writer] Generating comprehensive report with citations...")
        report = self._call_lm_studio(messages)
        
        # Ensure report is a string before processing
        if not isinstance(report, str):
            print(f"[writer] Warning: Report is not a string, got {type(report)}: {report}")
            report = str(report) if report else "Error: No content generated"
        
        # Add bibliography at the end if not already included
        if report and isinstance(report, str):
            # Check if report already contains references
            has_references = "References" in report or "Bibliography" in report
            if not has_references:
                bibliography = "\n\nReferences:\n\n"
                for citation_key, source_info in citations.items():
                    bibliography += f"{citation_key} {source_info['title']}\n"
                    bibliography += f"   Available at: {source_info['url']}\n\n"
                report += bibliography
        
        return report

if __name__ == "__main__":
    print("Enter your research question:")
    research_question = input("> ").strip()
    if not research_question:
        exit(1)

    # Run Planner Agent
    print("[system] Running planner agent...")
    planner = PlannerAgent()
    planner_result = planner.plan(research_question)
    subquestions = planner_result.get("subquestions", [])

    print(f"[system] Planner generated {len(subquestions)} subquestions.")
    print("Subquestions:")
    for i, subq in enumerate(subquestions):
        qid = subq.get("id", f"q{i+1}")
        qtype = subq.get("type", "unknown")
        text = subq.get("text", str(subq))
        print(f"  {i+1}. [{qid} - {qtype}] {text}")
    print()

    # Run Searcher Agent
    print("[system] Running searcher agent...")
    searcher = SearcherAgent()
    search_results = searcher.search_all(subquestions)

    print("\nSearch Results:")
    for qid, sources in search_results.items():
        print(f"\n{qid}:")
        for source in sources:
            print(f"  Title: {source['title']}")
            print(f"  URL: {source['url']}")
            print(f"  Content: {source['content'][:500]}{'...' if len(source['content']) > 500 else ''}")
            print(f"  Score: {source['score']}")
            print("  ---")
    print()

    # Run Writer Agent
    print("[system] Running writer agent...")
    writer = WriterAgent()
    report = writer.synthesize_report(research_question, subquestions, search_results)

    print("\n" + "="*80)
    print("SYNTHESIS REPORT")
    print("="*80)
    print(report)
    print("="*80)

    # Save report to file
    import uuid
    report_id = str(uuid.uuid4())[:8]
    filename = f"research_report_{report_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Research Question: {research_question}\n\n")
        f.write("Subquestions:\n")
        for i, subq in enumerate(subquestions):
            f.write(f"  {i+1}. {subq['text']}\n")
        f.write("\nSynthesis Report:\n")
        f.write(report)
    print(f"[writer] Saved full report to: {filename}")