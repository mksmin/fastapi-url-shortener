from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

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
) -> HTMLResponse:
    return form_response.render(
        request=request,
    )
