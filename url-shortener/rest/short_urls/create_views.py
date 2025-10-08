from collections.abc import Mapping
from typing import Any

from fastapi import (
    APIRouter,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from pydantic import BaseModel, ValidationError

from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrlCreate
from storage.short_urls.exceptions import ShortUrlAlreadyExistsError
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get(
    "/",
    name="short-urls:create-view",
)
def get_page_create_short_url(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = ShortUrlCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
    )
    return templates.TemplateResponse(
        request=request,
        name="short-urls/create.html",
        context=context,
    )


def format_pydantic_error(
    error: ValidationError,
) -> dict[str, str]:
    return {str(err["loc"][0]): err["msg"] for err in error.errors()}


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    *,
    form_validated: bool = True,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = ShortUrlCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=form_validated,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        request=request,
        name="short-urls/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@router.post(
    "/",
    name="short-urls:create",
    response_model=None,
)
async def create_short_url(
    request: Request,
    storage: GetShortUrlsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            short_url_create = ShortUrlCreate.model_validate(form)
        except ValidationError as e:
            errors = format_pydantic_error(e)
            return create_view_validation_response(
                request=request,
                errors=errors,
                form_data=form,
            )

    try:
        storage.create_or_raise_if_exists(
            short_url_create,
        )
    except ShortUrlAlreadyExistsError:
        errors = {
            "slug": f"Short URL with slug {short_url_create.slug} already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("short-urls:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return create_view_validation_response(
        request=request,
        errors=errors,
        form_data=short_url_create,
    )
