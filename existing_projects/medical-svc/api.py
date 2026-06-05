from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/agent")
async def medical_agent(item: Query):
    answer = f"Medical response to: {item.query}. Diabetes symptoms include thirst, frequent urination, and fatigue."
    return {"answer": answer, "model": "medical-rag-v1", "tokens_used": len(answer.split())}