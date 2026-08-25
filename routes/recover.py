from fastapi import APIRouter, HTTPException

from services.recovery import build_recovery_plan
from utils.errors import TrustLensError
from utils.privacy import safe_log
from utils.schemas import RecoveryRequest, RecoveryResponse

router = APIRouter(tags=["recover"])


@router.post("/recover", response_model=RecoveryResponse)
async def recover_endpoint(payload: RecoveryRequest) -> RecoveryResponse:
    try:
        safe_log("recover", incident_type=payload.incident_type)
        return build_recovery_plan(
            incident_type=payload.incident_type,
            description=payload.description,
            money_lost=payload.money_lost,
            shared_otp=payload.shared_otp,
            shared_personal_info=payload.shared_personal_info,
            contacted_via=payload.contacted_via,
        )
    except TrustLensError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
