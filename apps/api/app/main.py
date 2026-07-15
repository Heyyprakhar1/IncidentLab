from fastapi import FastAPI

from app.config import settings
from app.lifespan import lifespan
from app.middleware.request_logging import RequestLoggingMiddleware

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.add_middleware(RequestLoggingMiddleware)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }
