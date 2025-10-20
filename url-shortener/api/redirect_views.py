from fastapi import APIRouter
from starlette.responses import RedirectResponse

from dependencies.short_urls import ShortUrlBySlug

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_to_target_url(
    url: ShortUrlBySlug,
    slug: str,  # noqa: ARG001
) -> RedirectResponse:

    return RedirectResponse(
        url=str(url.target_url),
    )
