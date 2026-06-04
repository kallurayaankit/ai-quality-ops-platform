from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json
from pathlib import Path

app = FastAPI(title="AI Quality Ops Platform - QA as a Service")

# Request body
class RunRequest(BaseModel):
    target_endpoint: str
    test_plan: str = "test_plans/sample_plan.json"   # default

@app.post("/run")
async def run_tests(req: RunRequest):
    # Create a temporary test plan that points to the new endpoint
    with open(req.test_plan) as f:
        plan = json.load(f)

    # Override the target endpoint in the plan
    plan["target"]["endpoint"] = req.target_endpoint

    temp_plan_path = "test_plans/temp_plan.json"
    with open(temp_plan_path, "w") as f:
        json.dump(plan, f, indent=2)

    # Run the orchestrator with the temp plan
    # We'll call it as a subprocess (in Docker it will work)
    result = subprocess.run(
        ["python", "orchestrator/runner.py"],
        capture_output=True,
        text=True
    )

    # After running, check if reports exist
    summary_path = Path("reports/summary.html")
    if summary_path.exists():
        report_url = "/reports/summary.html"   # We'll serve static files
        return {
            "status": "completed",
            "exit_code": result.returncode,
            "report_url": report_url,
            "stdout": result.stdout[-1000:]  # last 1000 chars
        }
    else:
        raise HTTPException(status_code=500, detail="Report generation failed")

# Serve static reports (so you can open them in browser)
from fastapi.staticfiles import StaticFiles
app.mount("/reports", StaticFiles(directory="reports"), name="reports")