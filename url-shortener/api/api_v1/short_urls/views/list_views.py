from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
    background_task: BackgroundTasks,
) -> ShortUrl:
    short_url = storage.create(short_url_create)
    background_task.add_task(storage.save_state)
    return short_url
