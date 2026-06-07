import requests
import os

ZAP_ENDPOINT = os.getenv("ZAP_ENDPOINT", "http://zap:8000/scan")

def test_security_scan_passes_for_safe_target():
    resp = requests.post(ZAP_ENDPOINT, json={"target_url": "http://mock-ai:8000"})
    assert resp.status_code == 200
    data = resp.json()
    # The simulated scan should pass (no high‑risk vulnerabilities found)
    assert data["scan_passed"] == True, f"Security scan failed: {data}"