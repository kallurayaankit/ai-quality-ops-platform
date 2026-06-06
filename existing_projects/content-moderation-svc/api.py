from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/check")
async def check_content(item: TextInput):
    # Placeholder: return a safety score (0 = safe, 1 = harmful)
    text = item.text.lower()
    harmful_keywords = ["hacked", "kill", "bomb"]
    score = 1.0 if any(word in text for word in harmful_keywords) else 0.0
    return {"score": score, "flagged": score > 0.5}