import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
    Header,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from .crud import storage
from .redis import redis_tokens
from core.config import (
    USERS_DB,
    REDIS_TOKENS_SET_NAME,
)
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
static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](https://ya.ru)",
    auto_error=False,
)
user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username and password auth. [Read more](https://ya.ru)",
    auto_error=False,
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


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_tokens.sismember(
        REDIS_TOKENS_SET_NAME,
        api_token.credentials,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("API token: %s", api_token)

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(
        api_token=api_token,
    )


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_usafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):

    validate_basic_auth(
        credentials=credentials,
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)
    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth are required.",
    )
