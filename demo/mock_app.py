"""Bundled mock AI service for the demo.

Implements the exact contract the pillar tests expect:
    POST /agent  {"query": "..."}
    -> {"answer": "...", "tokens_used": int}
"""

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Mock RAG Agent")


class Query(BaseModel):
    query: str


FACTS = {
    "capital of france": "The capital of France is Paris.",
    "capital of japan": "The capital of Japan is Tokyo.",
    "capital of brazil": "The capital of Brazil is Brasilia.",
    "largest planet": "Jupiter is the largest planet in our solar system.",
    "boiling point of water": "Water boils at 100 degrees Celsius at sea level.",
}


@app.post("/agent")
def agent(q: Query):
    text = q.query.lower().strip()

    answer = None
    for key, fact in FACTS.items():
        if key in text:
            answer = fact
            break

    if answer is None:
        answer = f"Mock response to: {q.query}"

    return {
        "answer": answer,
        "tokens_used": len(answer.split()),
        "model": "mock-rag-v1",
    }


@app.get("/health")
def health():
    return {"status": "ok"}