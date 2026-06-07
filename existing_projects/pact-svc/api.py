from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI()

class ContractCheck(BaseModel):
    endpoint: str
    response: Dict[str, Any]
    expected_schema: Dict[str, Any]

@app.post("/validate")
async def validate_contract(check: ContractCheck):
    # Very simple contract check – just ensures required fields exist
    missing = []
    for field in check.expected_schema.get("required", []):
        if field not in check.response:
            missing.append(field)
    valid = len(missing) == 0
    return {
        "valid": valid,
        "missing_fields": missing,
        "message": "Contract is valid" if valid else f"Missing fields: {missing}"
    }