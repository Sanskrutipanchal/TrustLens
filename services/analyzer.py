from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from utils.schemas import AnalysisResponse

SCAM_KEYWORDS = (
    "otp",
    "one time password",
    "kyc",
    "blocked",
    "urgent",
    "immediately",
    "click here",
    "verify your account",
    "limited time",
    "congratulations",
    "lottery",
    "prize",
    "gift card",
    "investment return",
    "guaranteed profit",
    "send money",
    "upi pin",
    "cvv",
    "atm pin",
    "aadhaar update",
    "pan card update",
    "custom duty",
    "parcel held",
    "job offer",
    "work from home",
    "registration fee",
)

SUSPICIOUS_TLDS = {".xyz", ".top", ".click", ".zip", ".mov", ".gq", ".tk", ".ml", ".cf"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd"}

GENERIC_ACTIONS = [
    "Do not click unknown links or share OTP, PIN, or passwords.",
    "Verify the sender through an official app or website you already trust.",
    "If money moved, contact your bank or UPI app immediately.",
]


def analyze_text(text: str) -> AnalysisResponse:
    lowered = text.lower()
    hits = [keyword for keyword in SCAM_KEYWORDS if keyword in lowered]
    urgency = any(word in lowered for word in ("urgent", "immediately", "now", "blocked"))
    asks_secret = any(
        word in lowered for word in ("otp", "pin", "password", "cvv", "aadhaar", "pan")
    )

    score = min(1.0, 0.2 + 0.12 * len(hits) + (0.2 if urgency else 0) + (0.25 if asks_secret else 0))
    risk, verdict = _score_to_risk(score)
    signals = [f"Matched phrase: '{hit}'" for hit in hits[:6]]
    if urgency:
        signals.append("Uses urgency language to pressure a quick response.")
    if asks_secret:
        signals.append("Asks for secrets such as OTP, PIN, or identity numbers.")
    if not signals:
        signals.append("No strong scam phrases detected in this mock scan.")

    return AnalysisResponse(
        source_type="text",
        risk_level=risk,
        verdict=verdict,
        confidence=round(min(0.9, 0.45 + score / 2), 2),
        signals=signals,
        explanation=_explain(verdict, "message"),
        recommended_actions=_actions_for(risk),
        is_mock=True,
    )


def analyze_url(url: str) -> AnalysisResponse:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    signals: list[str] = []
    score = 0.15

    if parsed.scheme != "https":
        signals.append("URL is not using HTTPS.")
        score += 0.25
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host or ""):
        signals.append("Host is a raw IP address instead of a domain name.")
        score += 0.3
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
        signals.append("Domain uses a frequently abused top-level domain.")
        score += 0.25
    if host in SHORTENERS:
        signals.append("URL shortener can hide the real destination.")
        score += 0.2
    if host.count("-") >= 3 or host.count(".") >= 4:
        signals.append("Domain looks unusually long or hyphenated.")
        score += 0.15
    if any(brand in host and not host.endswith(f"{brand}.com") for brand in ("paypal", "amazon", "sbi", "hdfc", "icici")):
        signals.append("Domain may be impersonating a well-known brand.")
        score += 0.35
    if not signals:
        signals.append("No high-risk URL patterns found in this mock scan.")

    score = min(1.0, score)
    risk, verdict = _score_to_risk(score)
    return AnalysisResponse(
        source_type="url",
        risk_level=risk,
        verdict=verdict,
        confidence=round(min(0.88, 0.5 + score / 2), 2),
        signals=signals,
        explanation=_explain(verdict, "link"),
        recommended_actions=_actions_for(risk),
        is_mock=True,
    )


def analyze_document(path: Path, original_name: str, content_type: str | None) -> AnalysisResponse:
    """Heuristic mock scan. File contents are never logged or persisted."""
    suffix = path.suffix.lower()
    extracted = _read_text_safely(path)
    text_result = analyze_text(extracted) if extracted.strip() else None

    signals: list[str] = []
    score = 0.2
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        signals.append("Screenshot or image uploaded; mock scan used filename and type only.")
        lowered_name = original_name.lower()
        if any(word in lowered_name for word in ("otp", "kyc", "payment", "upi", "bank")):
            signals.append("Filename suggests a payment or identity screenshot.")
            score += 0.25
    elif suffix in {".pdf", ".txt", ".docx"}:
        signals.append("Document processed in memory for a mock keyword scan.")
        if text_result:
            signals.extend(text_result.signals[:4])
            score = max(score, {"low": 0.25, "medium": 0.55, "high": 0.85}[text_result.risk_level])
    else:
        signals.append("Unrecognized document type; treated as unknown risk.")
        score += 0.2

    if content_type and "octet-stream" in content_type:
        signals.append("Generic binary content type; treat with extra caution.")
        score += 0.1

    score = min(1.0, score)
    risk, verdict = _score_to_risk(score)
    return AnalysisResponse(
        source_type="document",
        risk_level=risk,
        verdict=verdict,
        confidence=round(min(0.8, 0.4 + score / 2), 2),
        signals=signals,
        explanation=_explain(verdict, "document"),
        recommended_actions=_actions_for(risk),
        is_mock=True,
    )


def _read_text_safely(path: Path) -> str:
    if path.suffix.lower() != ".txt":
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:20000]
    except OSError:
        return ""


def _score_to_risk(score: float) -> tuple[str, str]:
    if score >= 0.7:
        return "high", "likely_scam"
    if score >= 0.4:
        return "medium", "suspicious"
    return "low", "likely_safe"


def _explain(verdict: str, kind: str) -> str:
    if verdict == "likely_scam":
        return f"This {kind} shows several common scam patterns. Treat it as unsafe until verified through official channels."
    if verdict == "suspicious":
        return f"This {kind} has some warning signs. Pause before taking any action the sender requests."
    return f"This {kind} did not match strong scam patterns in the mock analyzer. Stay cautious anyway."


def _actions_for(risk: str) -> list[str]:
    if risk == "high":
        return [
            "Stop all communication with the sender.",
            "Do not transfer money or share OTP, PIN, Aadhaar, or PAN details.",
            "Report the incident at https://cybercrime.gov.in or call 1930.",
            *GENERIC_ACTIONS[:1],
        ]
    if risk == "medium":
        return [
            "Pause and independently verify the request using an official number or app.",
            *GENERIC_ACTIONS,
        ]
    return GENERIC_ACTIONS
