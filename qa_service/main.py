# Railway cache buster v2
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import json
from pathlib import Path

app = FastAPI(title="AI Quality Ops Platform - QA as a Service")

# Health check
@app.get("/")
async def root():
    return {"status": "alive", "service": "AI Quality Ops Platform"}

class RunRequest(BaseModel):
    target_endpoint: str
    test_plan: str = "test_plans/sample_plan.json"

@app.post("/run")
async def run_tests(req: RunRequest):
    with open(req.test_plan) as f:
        plan = json.load(f)

    plan["target"]["endpoint"] = req.target_endpoint

    temp_plan_path = "test_plans/temp_plan.json"
    with open(temp_plan_path, "w") as f:
        json.dump(plan, f, indent=2)

    result = subprocess.run(
        ["python", "orchestrator/runner.py", temp_plan_path],
        capture_output=True,
        text=True
    )

    summary_path = Path("reports/summary.html")
    if summary_path.exists():
        report_url = "/reports/summary.html"
        return {
            "status": "completed",
            "exit_code": result.returncode,
            "report_url": report_url,
            "stdout": result.stdout[-1000:]
        }
    else:
        raise HTTPException(status_code=500, detail="Report generation failed")

# Ensure required directories exist
os.makedirs("/app/reports", exist_ok=True)
os.makedirs("/app/qa_service/static", exist_ok=True)

# Serve static reports and UI
app.mount("/reports", StaticFiles(directory="/app/reports"), name="reports")
app.mount("/ui", StaticFiles(directory="/app/qa_service/static", html=True), name="ui")