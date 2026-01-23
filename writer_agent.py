import os, requests
from dotenv import load_dotenv


load_dotenv()


LMSTUDIO_URL = os.getenv("LMSTUDIO_URL")
MODEL = os.getenv("LOCAL_MODEL_NAME")
TIMEOUT = int(os.getenv("TIMEOUT", 180))


def write_final_summary(main_question, evidence_blocks):


    evidence_text = "\n\n".join(
        f"Sub-question: {e['sub_question']}\n"
        f"Evidence: {e['content']}"
        for e in evidence_blocks
    )


    prompt = f"""
You are an expert academic researcher and technical writer.


MAIN RESEARCH TOPIC:
{main_question}


EVIDENCE COLLECTED:
{evidence_text}


TASK:
Write a formal academic research report based on the evidence above.


CONSTRAINTS:
1. WORD COUNT: Minimum 450 words, Maximum 500 words. This is a strict requirement.
2. STRUCTURE: You MUST include exactly these sections in order:
   - Title
   - Abstract
   - Keywords
   - Introduction
   - Related Work
   - Methodology
   - Experiments & Results
   - Discussion
   - Conclusion & Future Work
   - References (List the sources from the evidence)


RULES:
- Use a formal, scholarly tone.
- Ensure the content flows logically between sections.
- Do not use URLs in the prose; keep them in the References section.
- Expand on the evidence to meet the word count while maintaining high academic quality.
"""


    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5, # Slightly higher for better flow and length
        "max_tokens": 2000
    }


    r = requests.post(
        f"{LMSTUDIO_URL}/v1/chat/completions",
        json=payload,
        timeout=TIMEOUT
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

