import requests
import os

FRAUD_ENDPOINT = os.getenv("FRAUD_ENDPOINT", "http://fraud-detection:8000/check")

def test_drift_check_returns_low_score():
    resp = requests.post(FRAUD_ENDPOINT, json={"avg_latency_ms": 200, "avg_tokens": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["drift_score"] <= 1.0
    assert data["drift_detected"] == False  # Normal conditions should not trigger drift