from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get(
    "/",
    name="short-urls:list",
    response_class=HTMLResponse,
)
def list_views(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="short-urls/list.html",
    )
