from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.api_v1.short_urls.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_storage_from_state()
    yield
