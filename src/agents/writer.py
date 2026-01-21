from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class WriterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("LLM_API_URL"),
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0.3
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert research writer who creates comprehensive, well-structured research reports.\\n\\n"
                "CRITICAL FORMATTING REQUIREMENTS:\\n"
                "- Use proper markdown formatting with headers, lists, tables, and emphasis\\n"
                "- Start with a compelling # Main Title (H1)\\n"
                "- Use ## for major sections (H2), ### for subsections (H3)\\n"
                "- Use **bold** for key terms and important points\\n"
                "- Use bullet points (-) for lists\\n"
                "- Use numbered lists (1., 2., 3.) for sequential information\\n"
                "- Use > for important quotes or key insights\\n"
                "- Use tables when comparing multiple items\\n"
                "- Add horizontal rules (---) between major sections\\n\\n"
                "CONTENT REQUIREMENTS:\\n"
                "- Write in a clear, engaging, professional tone\\n"
                "- Include an executive summary at the beginning\\n"
                "- Organize information logically with clear sections\\n"
                "- Provide specific examples and data points\\n"
                "- Include key findings and insights\\n"
                "- End with conclusions and recommendations\\n"
                "- Cite sources when mentioning specific information\\n\\n"
                "STRUCTURE TEMPLATE:\\n"
                "# [Research Topic]\\n\\n"
                "## Executive Summary\\n"
                "[Brief overview of key findings]\\n\\n"
                "## Introduction\\n"
                "[Context and background]\\n\\n"
                "## Key Findings\\n"
                "### [Finding 1]\\n"
                "[Details]\\n\\n"
                "### [Finding 2]\\n"
                "[Details]\\n\\n"
                "---\\n\\n"
                "## Detailed Analysis\\n"
                "[In-depth information]\\n\\n"
                "## Conclusions\\n"
                "[Summary and recommendations]\\n\\n"
                "## Sources\\n"
                "[List of references]"
            ),
            ("user", "Research results:\\n{results}\\n\\nCreate a comprehensive research report based on the above information.")
        ])

    def run(self, search_results):
        # Format search results for the prompt
        formatted_results = ""
        for idx, result in enumerate(search_results, 1):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            content = result.get("content", "")
            
            if content:
                formatted_results += f"\\n\\nSource {idx}:\\n"
                formatted_results += f"Title: {title}\\n"
                formatted_results += f"URL: {url}\\n"
                formatted_results += f"Content: {content[:1000]}\\n"
        
        if not formatted_results.strip():
            return "# Research Report\\n\\n## No Results\\n\\nNo research results were available to compile into a report."
        
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({"results": formatted_results})
