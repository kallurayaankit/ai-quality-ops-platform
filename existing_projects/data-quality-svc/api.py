from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class DatasetInfo(BaseModel):
    name: str
    row_count: int
    missing_values_pct: float = 0.0
    duplicate_rows_pct: float = 0.0

@app.post("/validate")
async def validate_dataset(info: DatasetInfo):
    issues = []
    if info.missing_values_pct > 5.0:
        issues.append("Too many missing values")
    if info.duplicate_rows_pct > 10.0:
        issues.append("Too many duplicate rows")
    if info.row_count < 1:
        issues.append("Dataset is empty")
    passed = len(issues) == 0
    return {
        "dataset": info.name,
        "passed": passed,
        "issues": issues
    }