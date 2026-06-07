import requests
import os

LOCUST_ENDPOINT = os.getenv("LOCUST_ENDPOINT", "http://locust:8000/run")

def test_locust_run_succeeds():
    resp = requests.post(LOCUST_ENDPOINT)
    assert resp.status_code == 200
    data = resp.json()
    # Basic check: we got some performance numbers
    assert "Average response time" in data or "error" not in data