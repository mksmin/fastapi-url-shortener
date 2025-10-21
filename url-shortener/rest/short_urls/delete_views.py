from fastapi import APIRouter, status
from fastapi.responses import Response

from dependencies.short_urls import GetShortUrlsStorage, ShortUrlBySlug

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.delete(
    "/",
    name="short-urls:delete",
)
def delete_short_url(
    short_url: ShortUrlBySlug,
    storage: GetShortUrlsStorage,
) -> Response:
    storage.delete(short_url)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
