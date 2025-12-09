from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextIn(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok", "message": "API is alive"}

@app.post("/moderate")
def moderate(payload: TextIn):
    # TEMP: just returns allowed=false if "kill yourself" or "kys" appears
    t = payload.text.lower().replace(" ", "")
    bad_phrases = ["killyourself", "kys", "goendyourself", "godie"]

    flagged = any(p in t for p in bad_phrases)

    return {
        "allowed": not flagged,
        "flagged": flagged,
        "debug": {"input": payload.text}
    }
 
