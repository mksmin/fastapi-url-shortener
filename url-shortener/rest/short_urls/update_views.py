from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from dependencies.short_urls import ShortUrlBySlug
from schemas.short_url import ShortUrlUpdate
from services.short_urls import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=ShortUrlUpdate,
    template_name="short-urls/update.html",
)


@router.get(
    "/",
    name="short-url:update-view",
)
def get_page_update_short_url(
    request: Request,
    short_url: ShortUrlBySlug,
) -> HTMLResponse:
    form = ShortUrlUpdate(**short_url.model_dump())
    return form_response.render(
        request=request,
        form_data=form,
        short_url=short_url,
    )
