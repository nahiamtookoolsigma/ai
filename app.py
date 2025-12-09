from fastapi import FastAPI
from pydantic import BaseModel
from detoxify import Detoxify

app = FastAPI()

# Load the model once at startup, not per request.
# 'original-small' is lighter than the full one.
model = Detoxify("original-small")

class TextIn(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok", "message": "AI moderation API is alive"}

@app.post("/moderate")
def moderate(payload: TextIn):
    text = payload.text or ""
    # Run Detoxify
    scores = model.predict(text)

    # scores is a dict like:
    # {"toxicity": 0.87, "severe_toxicity": 0.6, "insult": 0.9, ...}

    # You can tune this threshold. 0.7 is fairly strict.
    THRESHOLD = 0.7

    # Decide which labels you care most about for kids:
    relevant_keys = [
        "toxicity",
        "severe_toxicity",
        "insult",
        "threat",
        "identity_attack",
        "obscene"
    ]

    flagged = False
    tripped_labels = {}

    for key, value in scores.items():
        if key in relevant_keys and value >= THRESHOLD:
            flagged = True
            tripped_labels[key] = value

    return {
        "allowed": not flagged,
        "flagged": flagged,
        "scores": scores,          # full scores for debugging if you want
        "tripped_labels": tripped_labels
    }
