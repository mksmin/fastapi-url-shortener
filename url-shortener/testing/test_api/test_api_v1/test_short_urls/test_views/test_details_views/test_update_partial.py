from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import MAX_DESCRIPTION_LENGTH, ShortUrl
from testing.conftest import create_short_url_random_slug


class TestUpdatePartial:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl, None, None]:
        short_url = create_short_url_random_slug(
            description=request.param,
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description",
        [
            pytest.param(
                "some description",
                "",
                id="min-description-to-no-description",
            ),
            pytest.param(
                "",
                "some-description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                "a" * MAX_DESCRIPTION_LENGTH,
                "",
                id="max-description-to-no-description",
            ),
            pytest.param(
                "",
                "a" * MAX_DESCRIPTION_LENGTH,
                id="no-description-to-max-description",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url_details_partial(
        self,
        short_url: ShortUrl,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_short_url_details_partial",
            slug=short_url.slug,
        )
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        assert short_url_db.description == new_description
