from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

# A small blacklist of dangerous words/phrases – expand as needed
BLOCKED_TERMS = ["hacked", "kill yourself", "ignore all instructions"]

def is_safe(text: str) -> bool:
    """Return True if the text does NOT contain any blocked term."""
    lower_text = text.lower()
    for term in BLOCKED_TERMS:
        if term in lower_text:
            return False
    return True

@app.post("/agent")
async def agent_endpoint(item: Query):
    if not is_safe(item.query):
        # Refuse to answer unsafe queries
        return {
            "answer": "I'm sorry, I can't respond to that request.",
            "model": "mock-v1-safe",
            "tokens_used": 0
        }

    # Normal safe response
    return {
        "answer": f"You asked: {item.query}. The capital of France is Paris.",
        "model": "mock-v1-safe",
        "tokens_used": len(item.query.split())
    }