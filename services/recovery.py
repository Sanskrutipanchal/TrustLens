from utils.privacy import redact_sensitive
from utils.schemas import RecoveryAction, RecoveryResponse

HELPLINES = [
    "National Cybercrime Helpline: 1930",
    "Report online: https://cybercrime.gov.in",
    "Contact your bank or UPI app support from the official app, not from a message link.",
]


def build_recovery_plan(
    incident_type: str,
    description: str,
    money_lost: bool,
    shared_otp: bool,
    shared_personal_info: bool,
    contacted_via: str | None,
) -> RecoveryResponse:
    # Description is inspected for routing only; never logged or written to disk.
    _ = redact_sensitive(description)
    kind = incident_type.lower().strip()
    channel = (contacted_via or "unknown").lower()

    urgency = "medium"
    actions: list[RecoveryAction] = []

    if money_lost or shared_otp:
        urgency = "critical"
    elif shared_personal_info:
        urgency = "high"

    if money_lost:
        actions.append(
            RecoveryAction(
                priority="immediate",
                title="Freeze the transaction path",
                detail="Call your bank or UPI app from the number in the official app and ask to block the account, UPI ID, and recent transfers. Quote helpline 1930 if they need a cybercrime reference.",
            )
        )
        actions.append(
            RecoveryAction(
                priority="immediate",
                title="File a cybercrime report",
                detail="Report the fraud at https://cybercrime.gov.in or call 1930. Keep UTR/reference IDs, screenshots of chats, and the scammer's number or UPI ID.",
            )
        )

    if shared_otp:
        actions.append(
            RecoveryAction(
                priority="immediate",
                title="Assume the account is compromised",
                detail="Change passwords and app PINs for banking, email, and the app that received the OTP. Enable two-factor authentication on a new device if needed.",
            )
        )

    if shared_personal_info:
        actions.append(
            RecoveryAction(
                priority="soon",
                title="Watch identity misuse",
                detail="Monitor bank SMS, credit alerts, and government portals for unexpected KYC, PAN, or Aadhaar activity. Do not share more documents to 'reverse' the scam.",
            )
        )

    if "job" in kind:
        actions.append(
            RecoveryAction(
                priority="soon",
                title="Stop paying registration or training fees",
                detail="Legitimate employers do not ask for a job-processing fee over UPI or gift cards. Block the recruiter and report the listing.",
            )
        )
    elif "investment" in kind or "crypto" in kind:
        actions.append(
            RecoveryAction(
                priority="soon",
                title="Do not send recovery money",
                detail="Anyone offering to recover lost funds for an upfront fee is usually a second scam. Stick to your bank and official cybercrime channels.",
            )
        )
    elif "otp" in kind or "phishing" in kind or "upi" in kind:
        actions.append(
            RecoveryAction(
                priority="soon",
                title="Warn people in your circle",
                detail="Scammers often reuse the same script. Tell family not to trust similar messages from unknown numbers.",
            )
        )

    if channel in {"whatsapp", "sms", "call"}:
        actions.append(
            RecoveryAction(
                priority="follow_up",
                title="Block and report the number",
                detail="Block the sender on your phone and report the number inside WhatsApp/Truecaller or to your telecom provider.",
            )
        )

    actions.append(
        RecoveryAction(
            priority="follow_up",
            title="Preserve evidence privately",
            detail="Keep copies of chats and payment receipts on your own device. TrustLens does not store your documents or screenshots.",
        )
    )

    summary = _summary(urgency, money_lost, shared_otp)
    return RecoveryResponse(
        summary=summary,
        urgency=urgency,
        actions=actions,
        helplines=HELPLINES,
        is_mock=True,
    )


def _summary(urgency: str, money_lost: bool, shared_otp: bool) -> str:
    if urgency == "critical" and money_lost:
        return "Act now: money movement or OTP sharing means you should contact your bank and 1930 immediately."
    if shared_otp:
        return "OTP sharing is high risk. Lock down accounts first, then report the incident."
    if urgency == "high":
        return "Personal details may have been exposed. Secure accounts and monitor for misuse."
    return "Follow the steps below, verify every request independently, and report if anything still feels wrong."
