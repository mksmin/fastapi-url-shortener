import logging
from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from starlette import status

from .crud import storage
from schemas.short_url import ShortUrl

log = logging.getLogger(__name__)
UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    }
)


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
    request: Request,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage state")
        background_task.add_task(storage.save_state)
