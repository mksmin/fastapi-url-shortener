import logging

import uvicorn
from fastapi import (
    FastAPI,
)

from api import router as api_router
from api.main_views import router as main_views
from api.redirect_views import router as redirect_views
from app_lifespan import lifespan
from core.config import settings

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)

app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan,
)
app.include_router(redirect_views)
app.include_router(api_router)
app.include_router(main_views)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
