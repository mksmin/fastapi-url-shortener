from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from services.auth import redis_users

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    },
)
user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username and password auth. [Read more](https://ya.ru)",
    auto_error=False,
)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
) -> None:
    if credentials and redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )
