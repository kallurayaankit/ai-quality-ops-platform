from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class TestRequest(BaseModel):
    target_url: str

@app.post("/smoke")
async def run_smoke_tests(req: TestRequest):
    # Run a few basic regression checks against any endpoint
    results = []
    # Check 1: GET / (health)
    try:
        r = requests.get(req.target_url.rstrip("/") + "/", timeout=5)
        results.append({"test": "health", "passed": r.status_code == 200})
    except Exception as e:
        results.append({"test": "health", "passed": False, "error": str(e)})
    # Check 2: POST /agent with a query
    try:
        r = requests.post(req.target_url.rstrip("/") + "/agent", json={"query": "Hello"}, timeout=5)
        results.append({"test": "agent_query", "passed": r.status_code == 200 and "answer" in r.json()})
    except Exception as e:
        results.append({"test": "agent_query", "passed": False, "error": str(e)})
    return {"target": req.target_url, "results": results, "all_passed": all(r["passed"] for r in results)}