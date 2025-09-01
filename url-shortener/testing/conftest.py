import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        msg = "Environment is not ready for testing"
        pytest.exit(msg)


def build_short_url(
    slug: str,
    target_url: str = "https://example.com",
    description: str = "A short url",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=slug,
        target_url=target_url,
        description=description,
    )


def build_short_url_random_slug(
    target_url: str = "https://example.com",
    description: str = "A short url",
) -> ShortUrlCreate:
    return build_short_url(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        target_url=target_url,
        description=description,
    )


def create_short_url(
    slug: str,
    target_url: str = "https://example.com",
    description: str = "A short url",
) -> ShortUrl:
    short_url_in = build_short_url(
        slug=slug,
        target_url=target_url,
        description=description,
    )
    return storage.create(short_url_in)


def create_short_url_random_slug(
    description: str = "A short url", target_url: str = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_random_slug(
        target_url=target_url,
        description=description,
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl, None, None]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)
