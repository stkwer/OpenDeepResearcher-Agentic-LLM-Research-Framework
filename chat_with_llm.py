from openai import OpenAI
import sys

LOCAL_API_BASE = "http://127.0.0.1:1234/v1"
MODEL = "qwen2.5-1.5b-instruct"  

client = OpenAI(api_key="local", base_url=LOCAL_API_BASE)  
print("Local LLM connected. Type your message.")
print("Type 'exit' or Ctrl+C to quit.\n")

try:
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Bye")
            break

        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200,
            temperature=0.5,
        )

        try:
            reply = resp.choices[0].message.content
        except Exception:
      
            print("Raw response (unexpected shape):", resp)
            reply = None

        if reply:
            print("AI:", reply.strip(), "\n")
except KeyboardInterrupt:
    print("\nInterrupted. Bye.")
    sys.exit(0)
