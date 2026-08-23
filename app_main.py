from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re, os, json
import google.generativeai as genai
from PIL import Image
import io

app = FastAPI(title="TrustLens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

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
        "signals": [f"Matched phrase: '{kw}'" for kw in matched] or ["No scam phrases detected"],
        "explanation": "This message shows common scam patterns." if matched else "This message appears safe.",
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
    suspicious_words = ["verify", "secure", "login", "bank", "update", "account", "rbi", "kyc", "otp"]
    signals = []
    if any(tld in url for tld in suspicious_tlds):
        signals.append("Suspicious domain extension detected")
    if any(word in url for word in suspicious_words):
        signals.append("Suspicious keywords in URL")
    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
        signals.append("IP address used instead of domain name")
    if url.count('-') > 2:
        signals.append("Excessive hyphens in domain")
    if len(url) > 75:
        signals.append("Unusually long URL")
    score = len(signals) / 5
    if score > 0.4:
        risk, verdict, confidence = "high", "likely_phishing", min(0.95, 0.6 + score)
    elif score > 0.2:
        risk, verdict, confidence = "medium", "suspicious", 0.65
    else:
        risk, verdict, confidence = "low", "likely_safe", 0.75
    return {
        "risk_level": risk,
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "signals": signals or ["No suspicious patterns detected"],
        "explanation": "This URL shows phishing indicators." if signals else "This URL appears safe.",
        "recommended_actions": ["Do not click this link.", "Report at https://cybercrime.gov.in"] if signals else ["URL appears safe."],
        "is_mock": False
    }

@app.post("/analyze/voice")
def analyze_voice(input: VoiceInput):
    return analyze_text_logic(input.transcript)

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = '''Extract all text from this image and analyze if it contains scam or phishing content.
Respond ONLY with valid JSON in this exact format:
{"extracted_text":"text here","risk_level":"low","verdict":"likely_safe","confidence":0.5,"signals":["signal1"],"explanation":"explanation here","recommended_actions":["action1"],"is_mock":false}'''
        response = model.generate_content([prompt, image])
        text = response.text.strip()
        if "`" in text:
            text = text.split("`")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        return {"risk_level": "error", "verdict": "analysis_failed", "confidence": 0, "signals": [str(e)], "explanation": "Image analysis failed.", "recommended_actions": [], "is_mock": False}
