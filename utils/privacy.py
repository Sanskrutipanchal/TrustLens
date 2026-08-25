import logging
import re

logger = logging.getLogger("trustlens")

# Patterns used only to keep logs and stored artifacts free of secrets.
_AADHAAR = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
_PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE)
_OTP = re.compile(r"\b\d{4,8}\b")
_CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_UPI = re.compile(r"\b[\w.\-]+@[\w.\-]+\b")
_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE = re.compile(r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b")
_IFSC = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b", re.IGNORECASE)


def redact_sensitive(text: str) -> str:
    """Replace common identity and financial tokens before any logging."""
    if not text:
        return ""
    redacted = _AADHAAR.sub("[REDACTED_AADHAAR]", text)
    redacted = _PAN.sub("[REDACTED_PAN]", redacted)
    redacted = _CARD.sub("[REDACTED_CARD]", redacted)
    redacted = _IFSC.sub("[REDACTED_IFSC]", redacted)
    redacted = _EMAIL.sub("[REDACTED_EMAIL]", redacted)
    redacted = _UPI.sub("[REDACTED_UPI_OR_HANDLE]", redacted)
    redacted = _PHONE.sub("[REDACTED_PHONE]", redacted)
    redacted = _OTP.sub("[REDACTED_CODE]", redacted)
    return redacted


def safe_log(event: str, **metadata: object) -> None:
    """Log operational metadata only. Never pass document or message bodies here."""
    logger.info("%s | %s", event, metadata)
