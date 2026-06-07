import requests
import os

AB_ENDPOINT = os.getenv("AB_ENDPOINT", "http://model-ab-testing:8000/compare")

def test_ab_comparison_returns_two_models():
    resp = requests.post(AB_ENDPOINT, json={"query": "What is AI?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "model_a" in data
    assert "model_b" in data
    assert data["better_model"] in ["A", "B"]