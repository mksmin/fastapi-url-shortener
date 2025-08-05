import logging
from fastapi import HTTPException, BackgroundTasks
from starlette import status

from .crud import storage
from schemas.short_url import ShortUrl

log = logging.getLogger(__name__)


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Slug {slug!r} not found",
    )


def save_storage_state(
    background_task: BackgroundTasks,
):
    yield
    log.info("Again inside dependency save_storage_state")
    background_task.add_task(storage.save_state)
