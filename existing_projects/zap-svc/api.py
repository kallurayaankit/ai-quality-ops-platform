from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class ScanRequest(BaseModel):
    target_url: str

@app.post("/scan")
async def run_scan(req: ScanRequest):
    # Simulate a security scan – replace with real ZAP integration later
    vulnerabilities = [
        {"name": "XSS", "risk": "Medium", "found": random.choice([True, False])},
        {"name": "SQL Injection", "risk": "High", "found": random.choice([True, False])},
        {"name": "Sensitive Data Exposure", "risk": "Medium", "found": False},
    ]
    return {
        "target": req.target_url,
        "vulnerabilities": vulnerabilities,
        "scan_passed": not any(v["found"] for v in vulnerabilities if v["risk"] == "High")
    }