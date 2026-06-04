import requests
import os
import os
ENDPOINT = os.getenv("TARGET_ENDPOINT", "http://localhost:8000/agent")

def test_answer_contains_correct_fact():
    response = requests.post(ENDPOINT, json={"query": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert "Paris" in data["answer"], f"Expected 'Paris' in answer, got: {data['answer']}"

def test_response_has_required_fields():
    response = requests.post(ENDPOINT, json={"query": "Hello"})
    data = response.json()
    assert "answer" in data
    assert "tokens_used" in data
    assert isinstance(data["tokens_used"], int)