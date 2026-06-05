import requests
import os

RESEARCH_ENDPOINT = os.getenv("RESEARCH_ENDPOINT", "http://research-agent:8000/agent")

def test_research_agent_returns_structured_answer():
    query = "Tell me about climate change impacts"
    resp = requests.post(RESEARCH_ENDPOINT, json={"query": query})
    assert resp.status_code == 200
    data = resp.json()
    answer = data["answer"].lower()
    assert "conclusion" in answer or "source" in answer, f"Answer lacked expected structure: {answer}"
    assert "sources_used" in data
    assert data["sources_used"] > 0