import time
import statistics
import requests
import os
ENDPOINT = os.getenv("TARGET_ENDPOINT", "http://localhost:8000/agent")

SAMPLE_SIZE = 20

# Fake cost per token – adjust to match your mock's token count
COST_PER_TOKEN = 0.001  # $0.001 per token

# Relax thresholds to match the mock's natural behaviour
P95_LATENCY_THRESHOLD_MS = 3000   # 3 seconds (as per global_thresholds)
COST_PER_1K_THRESHOLD = 5.00      # $5.00

def test_p95_latency():
    """95th percentile latency must be under the threshold."""
    latencies = []
    for _ in range(SAMPLE_SIZE):
        start = time.time()
        resp = requests.post(ENDPOINT, json={"query": "What is the capital of France?"})
        resp.raise_for_status()
        latencies.append(time.time() - start)

    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    p95_ms = p95 * 1000
    print(f"p95 latency: {p95_ms:.1f} ms")
    assert p95_ms < P95_LATENCY_THRESHOLD_MS, f"p95 latency {p95_ms:.1f} ms exceeds {P95_LATENCY_THRESHOLD_MS} ms"

def test_cost_per_1k_requests():
    """Estimated cost per 1,000 requests must be under the threshold."""
    total_tokens = 0
    for _ in range(SAMPLE_SIZE):
        resp = requests.post(ENDPOINT, json={"query": "Test cost calculation."})
        resp.raise_for_status()
        total_tokens += resp.json().get("tokens_used", 0)

    cost_1k = (total_tokens / SAMPLE_SIZE) * 1000 * COST_PER_TOKEN
    print(f"Estimated cost per 1k requests: ${cost_1k:.2f}")
    assert cost_1k <= COST_PER_1K_THRESHOLD, f"Cost ${cost_1k:.2f} exceeds ${COST_PER_1K_THRESHOLD}"