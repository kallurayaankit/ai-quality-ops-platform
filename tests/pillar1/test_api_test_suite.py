import requests
import os

API_SUITE_ENDPOINT = os.getenv("API_SUITE_ENDPOINT", "http://api-test-suite:8000/smoke")

def test_smoke_tests_pass_on_mock_ai():
    resp = requests.post(API_SUITE_ENDPOINT, json={"target_url": "http://mock-ai:8000"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["all_passed"] == True, f"Smoke tests failed: {data}"