import time
import json
import requests
from pathlib import Path
import os
ENDPOINT = os.getenv("TARGET_ENDPOINT", "http://localhost:8000/agent")

SAMPLE_SIZE = 10

BASELINE_PATH = Path("test_plans/baseline_metrics.json")
LATEST_PATH   = Path("test_plans/latest_metrics.json")

def collect_metrics(n_requests: int):
    latencies = []
    tokens = []
    for _ in range(n_requests):
        start = time.time()
        resp = requests.post(ENDPOINT, json={"query": "Hello"})
        resp.raise_for_status()
        latencies.append((time.time() - start) * 1000)  # ms
        tokens.append(resp.json().get("tokens_used", 0))
    return {
        "avg_latency_ms": sum(latencies) / len(latencies),
        "avg_tokens_per_request": sum(tokens) / len(tokens)
    }

def test_metrics_are_logged():
    """Ensure we can collect and save run metrics."""
    metrics = collect_metrics(SAMPLE_SIZE)
    LATEST_PATH.parent.mkdir(exist_ok=True)
    with open(LATEST_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved: latency={metrics['avg_latency_ms']:.1f}ms, tokens={metrics['avg_tokens_per_request']:.1f}")
    assert LATEST_PATH.exists()

def test_no_performance_drift():
    """Current run must not deviate too much from baseline."""
    # Load baseline (if missing, skip test)
    if not BASELINE_PATH.exists():
        print("No baseline found – skipping drift check.")
        return

    with open(BASELINE_PATH) as f:
        baseline = json.load(f)

    current = collect_metrics(SAMPLE_SIZE)

    # Allowed drift: latency max +100%, tokens max +50%
    latency_change = (current["avg_latency_ms"] - baseline["avg_latency_ms"]) / baseline["avg_latency_ms"]
    token_change   = (current["avg_tokens_per_request"] - baseline["avg_tokens_per_request"]) / baseline["avg_tokens_per_request"]

    print(f"Latency drift: {latency_change*100:.1f}%  (baseline {baseline['avg_latency_ms']}ms → {current['avg_latency_ms']:.1f}ms)")
    print(f"Token   drift: {token_change*100:.1f}%  (baseline {baseline['avg_tokens_per_request']} → {current['avg_tokens_per_request']:.1f})")

    assert latency_change < 1.0, f"Latency drift too high: {latency_change*100:.1f}%"
    assert token_change < 0.5,  f"Token drift too high: {token_change*100:.1f}%"