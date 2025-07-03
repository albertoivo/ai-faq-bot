from fastapi import FastAPI

from app.api import faq
from app.config.logging import setup_logging

logger = setup_logging()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(faq.router)

@app.get("/", tags=["Home"], summary="Initial Route")
def home():
    logger.info("Home route accessed")
    return {"detail": "AI FAQ Bot API running..."}


@app.get("/health", tags=["Home"], summary="Health Check")
def health_check():
    logger.info("Health check route accessed")
    return {"status": "healthy"}

@app.get("/version", tags=["Home"], summary="Version Check")
def version_check():
    logger.info("Version check route accessed")
    return {"version": "1.0.0", "description": "AI FAQ Bot API version 1.0.0"}