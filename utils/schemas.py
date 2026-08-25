from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

RiskLevel = Literal["low", "medium", "high"]
Verdict = Literal["likely_safe", "suspicious", "likely_scam"]


class TextAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class UrlAnalyzeRequest(BaseModel):
    url: HttpUrl


class RecoveryRequest(BaseModel):
    incident_type: str = Field(
        ...,
        min_length=1,
        max_length=80,
        description="e.g. phishing, fake_job, upi_fraud, otp_scam, investment_scam",
    )
    description: str = Field(..., min_length=1, max_length=5000)
    money_lost: bool = False
    shared_otp: bool = False
    shared_personal_info: bool = False
    contacted_via: str | None = Field(
        default=None,
        max_length=80,
        description="e.g. sms, whatsapp, email, call, social_media",
    )


class AnalysisResponse(BaseModel):
    source_type: Literal["text", "url", "document"]
    risk_level: RiskLevel
    verdict: Verdict
    confidence: float = Field(..., ge=0, le=1)
    signals: list[str]
    explanation: str
    recommended_actions: list[str]
    is_mock: bool = True


class RecoveryAction(BaseModel):
    priority: Literal["immediate", "soon", "follow_up"]
    title: str
    detail: str


class RecoveryResponse(BaseModel):
    summary: str
    urgency: Literal["low", "medium", "high", "critical"]
    actions: list[RecoveryAction]
    helplines: list[str]
    is_mock: bool = True


class HealthResponse(BaseModel):
    status: str
    service: str
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: str
