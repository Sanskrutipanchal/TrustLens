from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from services.analyzer import analyze_document, analyze_text, analyze_url
from services.file_handler import delete_temp_file, save_upload
from utils.errors import TrustLensError
from utils.privacy import safe_log
from utils.schemas import AnalysisResponse, TextAnalyzeRequest, UrlAnalyzeRequest

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("/text", response_model=AnalysisResponse)
async def analyze_text_endpoint(payload: TextAnalyzeRequest) -> AnalysisResponse:
    try:
        safe_log("analyze_text")
        return analyze_text(payload.text)
    except TrustLensError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/url", response_model=AnalysisResponse)
async def analyze_url_endpoint(payload: UrlAnalyzeRequest) -> AnalysisResponse:
    try:
        safe_log("analyze_url")
        return analyze_url(str(payload.url))
    except TrustLensError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/document", response_model=AnalysisResponse)
async def analyze_document_endpoint(file: UploadFile = File(...)) -> AnalysisResponse:
    temp_path: Path | None = None
    try:
        temp_path = await save_upload(file)
        safe_log("analyze_document", extension=temp_path.suffix.lower())
        return analyze_document(temp_path, file.filename or "upload", file.content_type)
    except TrustLensError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    finally:
        delete_temp_file(temp_path)
