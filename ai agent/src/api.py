from fastapi import FastAPI
from pydantic import BaseModel
from src.core.langgraph_pipeline import build_graph

app = FastAPI()
graph = build_graph()


class Prompt(BaseModel):
    message: str


@app.post("/chat")
def chat(prompt: Prompt):
    result = graph.invoke({"query": prompt.message})
    return {
        "reply": result["answer"],
        "plan": result["plan"]
    }
