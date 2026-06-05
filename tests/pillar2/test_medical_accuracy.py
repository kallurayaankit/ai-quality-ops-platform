import requests
import os

# Use environment variable, default to localhost for local runs
MEDICAL_ENDPOINT = os.getenv("MEDICAL_ENDPOINT", "http://medical-qa:8000/agent")

def test_medical_answer_contains_fact():
    question = "What are the symptoms of diabetes?"
    resp = requests.post(MEDICAL_ENDPOINT, json={"query": question})
    assert resp.status_code == 200
    data = resp.json()
    answer = data["answer"].lower()
    # Basic check: the answer should mention common symptoms
    assert "thirst" in answer or "urination" in answer or "fatigue" in answer, f"Answer did not contain expected medical facts: {answer}"