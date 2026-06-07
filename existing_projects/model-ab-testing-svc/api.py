from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/compare")
async def compare_models(item: Query):
    # Simulate two model versions returning slightly different answers
    model_a = f"Model A answer to: {item.query} (score: 0.95)"
    model_b = f"Model B answer to: {item.query} (score: 0.88)"
    # randomly decide if B is worse (for regression detection)
    better = "A" if random.random() > 0.2 else "B"
    return {
        "model_a": model_a,
        "model_b": model_b,
        "better_model": better,
        "difference_detected": better != "A"
    }