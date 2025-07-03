from fastapi import FastAPI

from app.config.logging import setup_logging

logger = setup_logging()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/", tags=["Home"], summary="Initial Route")
def home():
    logger.info("Home route accessed")
    return {"detail": "AI FAQ Bot API running..."}


@app.get("/health", tags=["Home"], summary="Health Check")
def health_check():
    logger.info("Health check route accessed")
    return {"status": "healthy"}
