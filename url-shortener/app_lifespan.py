from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.short_urls import ShortUrlsStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.short_urls_storage = ShortUrlsStorage(
        hash_name=settings.redis.collections_names.short_urls_hash,
    )
    yield
