from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/api")
@app.get("/api/")
def root():
    return {"status": "TrustLens API is running"}


@app.post("/api/analyze/text")
def analyze_text(request: TextRequest):
    text = request.text.lower()

    scam_keywords = [
        "urgent",
        "otp",
        "verify",
        "blocked",
        "kyc",
        "click here",
        "winner",
        "prize",
        "bank account",
        "password",
        "suspended",
    ]

    matches = [word for word in scam_keywords if word in text]

    if matches:
        return {
            "risk": "HIGH",
            "message": "Potential scam detected",
            "matched_keywords": matches,
        }

    return {
        "risk": "LOW",
        "message": "No obvious scam indicators detected",
        "matched_keywords": [],
    }