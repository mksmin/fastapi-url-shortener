from fastapi import HTTPException
from starlette import status

from .crud import storage
from schemas.short_url import ShortUrl


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
