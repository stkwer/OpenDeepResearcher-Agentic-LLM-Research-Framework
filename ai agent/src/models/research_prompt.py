def build_research_prompt(topic: str) -> str:
    return f"""
You are an academic research writer.

Write a FULL LENGTH research paper on the topic:

"{topic}"

STRICT REQUIREMENTS:
- Write in formal academic tone
- Minimum 1500–2000 words
- Follow EXACT research paper structure
- Do NOT write questions inside sections
- Do NOT summarize briefly
- Expand each section with depth and examples

FORMAT (MANDATORY):

Title

Abstract
(150–200 words)

Keywords
(5–7 keywords)

1. Introduction
(Background, motivation, scope)

2. Literature Review
(Existing studies, trends, gaps)

3. Methodology / Approach
(Conceptual or analytical approach)

4. Applications / Use Cases
(Detailed real-world examples)

5. Challenges and Limitations
(Technical, ethical, societal)

6. Future Scope
(Emerging trends, opportunities)

7. Conclusion
(Summary of findings)

References
(Numbered list with URLs)

IMPORTANT:
- Use academic language
- No bullet-point-only answers
- Write like a real journal paper
"""
