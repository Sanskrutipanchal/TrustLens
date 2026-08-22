import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from routes.analyze import router as analyze_router
from routes.recover import router as recover_router
from utils.config import settings
from utils.errors import TrustLensError
from utils.privacy import safe_log
from utils.schemas import HealthResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("trustlens")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings.temp_upload_dir.mkdir(parents=True, exist_ok=True)
    safe_log("startup", env=settings.app_env)
    yield
    safe_log("shutdown")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered digital safety guardian. Uploaded files are analyzed in a temp folder and deleted immediately.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(recover_router)


@app.get("/", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        message="TrustLens API is running",
    )


@app.exception_handler(TrustLensError)
async def trustlens_error_handler(_: Request, exc: TrustLensError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": "request_failed", "detail": exc.message})


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return JSONResponse(status_code=exc.status_code, content={"error": "http_error", "detail": detail})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Do not echo submitted text, URLs, or file fields back to logs or clients.
    safe_log("validation_error")
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": "Invalid request. Check required fields and file type."},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error: %s", type(exc).__name__)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": "Something went wrong. The uploaded file was not kept."},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
