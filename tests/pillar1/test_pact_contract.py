import requests
import os

PACT_ENDPOINT = os.getenv("PACT_ENDPOINT", "http://pact:8000/validate")

def test_valid_contract_passes():
    resp = requests.post(PACT_ENDPOINT, json={
        "endpoint": "/agent",
        "response": {"answer": "Hello", "tokens_used": 5},
        "expected_schema": {"required": ["answer", "tokens_used"]}
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] == True, f"Contract should be valid: {data}"

def test_missing_field_fails_contract():
    resp = requests.post(PACT_ENDPOINT, json={
        "endpoint": "/agent",
        "response": {"answer": "Hello"},
        "expected_schema": {"required": ["answer", "tokens_used"]}
    })
    data = resp.json()
    assert data["valid"] == False, f"Contract should be invalid due to missing field: {data}"