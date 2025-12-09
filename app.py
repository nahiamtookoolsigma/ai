# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from detoxify import Detoxify

app = FastAPI()

# Load model once at startup
model = Detoxify("original")  # consider 'small' or lighter variant if memory is tight

class TextIn(BaseModel):
    text: str

@app.post("/moderate")
def moderate(payload: TextIn):
    # Run toxicity prediction
    scores = model.predict(payload.text)
    # scores is a dict like {"toxicity": 0.87, "insult": 0.9, ...}

    # Simple policy: block if any key is above some threshold
    threshold = 0.7
    flagged = any(score >= threshold for score in scores.values())

    return {
        "allowed": not flagged,
        "flagged": flagged,
        "scores": scores
    }
