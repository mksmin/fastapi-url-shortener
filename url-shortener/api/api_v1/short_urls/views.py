from typing import Annotated

from fastapi import Depends, APIRouter

from .dependencies import (
    prefetch_short_url,
)
from .crud import SHORT_URLS
from schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


@router.get(
    "/{slug}",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return url
