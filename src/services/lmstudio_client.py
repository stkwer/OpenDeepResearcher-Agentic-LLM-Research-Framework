from openai import OpenAI
from src.config import settings

# Client that talks to LM Studio's OpenAI-compatible server
client = OpenAI(
    base_url=settings.LMSTUDIO_BASE_URL,
    api_key=settings.LMSTUDIO_API_KEY,  # LM Studio just needs any non-empty string
)


def chat_with_lmstudio(message: str) -> str:
    """Send a single message to the local LLM and return its reply."""
    response = client.chat.completions.create(
        model=settings.LMSTUDIO_MODEL,
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content
