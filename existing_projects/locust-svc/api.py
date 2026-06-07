from fastapi import FastAPI
import subprocess, os, json, tempfile

app = FastAPI()
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/run")
async def run_locust():
    # Run Locust headless against the target endpoint
    target = os.getenv("TARGET_ENDPOINT", "http://mock-ai:8000")
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_prefix = os.path.join(tmpdir, "stats")
        subprocess.run([
            "locust", "-f", "locustfile.py",
            "--headless",
            "--host", target,
            "--users", "5",
            "--spawn-rate", "1",
            "--run-time", "10s",
            "--csv", csv_prefix,
            "--only-summary"
        ], check=True, cwd="/app")
        # Read the summary CSV
        stats_path = f"{csv_prefix}_stats.csv"
        with open(stats_path) as f:
            lines = f.readlines()
        # Return the first data line as JSON (very basic)
        if len(lines) > 1:
            headers = lines[0].strip().split(",")
            values = lines[1].strip().split(",")
            result = dict(zip(headers, values))
        else:
            result = {"error": "No data"}
        return result