from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class MetricsInput(BaseModel):
    avg_latency_ms: float = 200.0
    avg_tokens: float = 3.0

@app.post("/check")
async def check_drift(item: MetricsInput):
    # Simulate drift detection: return a drift score between 0 and 1
    # In a real project you'd compare to a baseline or model
    score = random.uniform(0, 0.1)  # low drift by default
    return {"drift_score": score, "drift_detected": score > 0.5}