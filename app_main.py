from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

# Load variables from .env
load_dotenv()

app = FastAPI(title="TrustLens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://trust-lens-lake.vercel.app",
        "https://trust-lens-git-frontend-branch-four-sights.vercel.app",
         allow_methods=["*"],
    ],

    allow_headers=["*"],
)

# Initialize Gemini client using the API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

SCAM_KEYWORDS = [
    "urgent", "immediately", "blocked", "kyc", "otp", "verify",
    "transfer", "bank account", "click here", "free", "winner",
    "prize", "lottery", "suspended", "limited time", "act now",
    "congratulations", "rbi", "income tax", "police", "arrest",
    "password", "pin", "aadhaar", "pan", "suspicious", "phishing"
]


def analyze_text_logic(text: str):
    lower = text.lower()
    matched = [kw for kw in SCAM_KEYWORDS if kw in lower]
    score = len(matched) / len(SCAM_KEYWORDS)

    if score > 0.3:
        risk, verdict, confidence = "high", "likely_scam", min(0.95, 0.6 + score)
    elif score > 0.1:
        risk, verdict, confidence = "medium", "suspicious", 0.6 + score
    else:
        risk, verdict, confidence = "low", "likely_safe", max(0.4, 0.7 - score)

    return {
        "risk_level": risk,
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "signals": [
            f"Matched phrase: '{kw}'" for kw in matched
        ] or ["No scam phrases detected"],
        "explanation": (
            "This message shows common scam patterns."
            if matched
            else "This message appears safe."
        ),
        "recommended_actions": [
            "Stop all communication with the sender.",
            "Do not transfer money or share OTP, PIN, Aadhaar, or PAN details.",
            "Report at https://cybercrime.gov.in or call 1930.",
        ] if matched else ["No action needed."],
        "is_mock": False
    }


class TextInput(BaseModel):
    text: str


class UrlInput(BaseModel):
    url: str


class VoiceInput(BaseModel):
    transcript: str


@app.get("/")
def root():
    return {"status": "TrustLens API running"}


@app.post("/analyze/text")
def analyze_text(input: TextInput):
    return analyze_text_logic(input.text)


@app.post("/analyze/url")
def analyze_url(input: UrlInput):
    url = input.url.lower()

    suspicious_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf", ".gq"]
    suspicious_words = [
        "verify", "secure", "login", "bank",
        "update", "account", "rbi", "kyc", "otp"
    ]

    signals = []

    if any(tld in url for tld in suspicious_tlds):
        signals.append("Suspicious domain extension detected")

    if any(word in url for word in suspicious_words):
        signals.append("Suspicious keywords in URL")

    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
        signals.append("IP address used instead of domain name")

    if url.count("-") > 2:
        signals.append("Excessive hyphens in domain")

    if len(url) > 75:
        signals.append("Unusually long URL")

    score = len(signals) / 5

    if score > 0.4:
        risk, verdict, confidence = (
            "high",
            "likely_phishing",
            min(0.95, 0.6 + score)
        )
    elif score > 0.2:
        risk, verdict, confidence = "medium", "suspicious", 0.65
    else:
        risk, verdict, confidence = "low", "likely_safe", 0.75

    return {
        "risk_level": risk,
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "signals": signals or ["No suspicious patterns detected"],
        "explanation": (
            "This URL shows phishing indicators."
            if signals
            else "This URL appears safe."
        ),
        "recommended_actions": (
            ["Do not click this link.", "Report at https://cybercrime.gov.in"]
            if signals
            else ["URL appears safe."]
        ),
        "is_mock": False
    }


@app.post("/analyze/voice")
def analyze_voice(input: VoiceInput):
    return analyze_text_logic(input.transcript)


@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Validate uploaded image
        Image.open(io.BytesIO(contents))

        prompt = """
Extract all text from this image and analyze whether it contains
scam, fraud, phishing, financial fraud, impersonation, or suspicious
content.

Respond ONLY with valid JSON in this exact format:

{
  "extracted_text": "text found in image",
  "risk_level": "low",
  "verdict": "likely_safe",
  "confidence": 0.5,
  "signals": ["signal1"],
  "explanation": "explanation here",
  "recommended_actions": ["action1"],
  "is_mock": false
}

Use:
- risk_level: "low", "medium", or "high"
- verdict: "likely_safe", "suspicious", "likely_scam", or "likely_phishing"
- confidence: number between 0 and 1
- signals: list of specific suspicious indicators
- recommended_actions: practical safety actions
"""

        mime_type = file.content_type or "image/jpeg"

        image_part = types.Part.from_bytes(
            data=contents,
            mime_type=mime_type
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[prompt, image_part]
        )

        text = response.text.strip()

        # Remove Markdown code fences if Gemini returns them
        if text.startswith("```"):
            text = text.replace("```json", "", 1)
            text = text.replace("```", "")
            text = text.strip()

        result = json.loads(text)

        return result

    except Exception as e:
        return {
            "risk_level": "error",
            "verdict": "analysis_failed",
            "confidence": 0,
            "signals": [str(e)],
            "explanation": "Image analysis failed.",
            "recommended_actions": [],
            "is_mock": False
        }


class ChatRequest(BaseModel):
    user_message: str

@app.post("/api/v1/chat/verify")
def chat_verify(payload: ChatRequest):
    text = payload.user_message.lower()
    import re
    tokens = re.findall(r'\b\w+\b', text)
    cred_hits = sum(1 for t in tokens if t in ["otp","pin","password","cvv","card","netbanking","login"])
    id_hits = sum(1 for t in tokens if t in ["aadhaar","pan","passport","kyc","documents"])
    urgency_hits = sum(1 for t in tokens if t in ["urgent","immediately","suspended","blocked","won","lottery"])
    has_url = 1.0 if re.search(r'(http|www|\\.com|\\.in)', text) else 0.0
    score = min((cred_hits*40)+(id_hits*35)+(urgency_hits*15)+(has_url*10), 100)
    labels = []
    if cred_hits: labels.append("Credential Exfiltration")
    if id_hits: labels.append("Identity Harvesting")
    if urgency_hits: labels.append("Social Engineering")
    if has_url: labels.append("External Redirect")
    if score >= 70:
        tier, action = "CRITICAL RISK", "HALT. Do not share credentials or open links."
        explanation = f"High risk detected: {', '.join(labels)}"
    elif score >= 20:
        tier, action = "SUSPICIOUS", "Verify through official channels."
        explanation = f"Caution: {', '.join(labels)}"
    else:
        tier, action = "VERIFIED SAFE", "Safe to interact."
        explanation = "No scam patterns detected."
    return {"risk_score": score, "risk_tier": tier, "extracted_vectors": labels, "safest_next_action": action, "ai_explanation": explanation}


class ChatRequest(BaseModel):
    user_message: str

@app.post('/api/v1/chat/verify')
def chat_verify(payload: ChatRequest):
    return analyze_text_logic(payload.user_message)
