import requests
import os

DQ_ENDPOINT = os.getenv("DQ_ENDPOINT", "http://data-quality:8000/validate")

def test_clean_dataset_passes_validation():
    resp = requests.post(DQ_ENDPOINT, json={
        "name": "test-dataset",
        "row_count": 100,
        "missing_values_pct": 1.0,
        "duplicate_rows_pct": 2.0
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] == True, f"Validation failed unexpectedly: {data}"

def test_dirty_dataset_fails_validation():
    resp = requests.post(DQ_ENDPOINT, json={
        "name": "bad-dataset",
        "row_count": 50,
        "missing_values_pct": 15.0,
        "duplicate_rows_pct": 25.0
    })
    data = resp.json()
    assert data["passed"] == False, f"Dirty dataset should have failed validation: {data}"