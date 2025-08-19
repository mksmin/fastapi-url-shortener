from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl
from testing.test_api.test_api_v1.test_short_urls.test_crud import create_short_url

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


@pytest.fixture()
def short_url() -> Generator[ShortUrl, None, None]:
    short_url = create_short_url()
    yield short_url
    storage.delete(short_url)
