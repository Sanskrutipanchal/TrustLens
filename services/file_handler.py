from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from utils.config import settings
from utils.errors import FileProcessingError, InvalidInputError
from utils.privacy import safe_log

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


async def save_upload(upload: UploadFile) -> Path:
    original_name = upload.filename or "upload"
    suffix = Path(original_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise InvalidInputError(
            "Unsupported file type. Upload a PDF, Word, text, or image file."
        )

    content_type = (upload.content_type or "").split(";")[0].strip().lower()
    if content_type and content_type not in ALLOWED_CONTENT_TYPES and content_type != "application/octet-stream":
        raise InvalidInputError("Unsupported file content type.")

    data = await upload.read()
    if not data:
        raise InvalidInputError("Uploaded file is empty.")
    if len(data) > settings.max_upload_bytes:
        raise InvalidInputError(
            f"File is too large. Maximum size is {settings.max_upload_mb} MB."
        )

    temp_path = settings.temp_upload_dir / f"{uuid4().hex}{suffix}"
    try:
        temp_path.write_bytes(data)
    except OSError as exc:
        raise FileProcessingError("Could not store the file temporarily for analysis.") from exc

    safe_log(
        "temp_file_saved",
        bytes=len(data),
        extension=suffix,
        content_type=content_type or "unknown",
    )
    return temp_path


def delete_temp_file(path: Path | None) -> None:
    if path is None:
        return
    try:
        if path.exists():
            path.unlink()
            safe_log("temp_file_deleted", extension=path.suffix.lower())
    except OSError:
        safe_log("temp_file_delete_failed", extension=path.suffix.lower())
