import random
import string
from collections.abc import Generator
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.short_urls.crud import ShortUrlAlreadyExistsError, storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description="test-description",
        target_url="https://example.com",
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    yield short_url
    storage.delete(short_url)


class ShortUrlStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.short_url = create_short_url()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(
            **self.short_url.model_dump(),
        )
        source_description = self.short_url.description
        short_url_update.description *= 2
        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_in=short_url_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**updated_short_url.model_dump()),
        )
        self.assertEqual(
            short_url_update.description,
            updated_short_url.description,
        )

    def test_update_partial(self) -> None:
        short_url_partial_update = ShortUrlPartialUpdate(
            description=self.short_url.description * 2,
        )
        source_description = self.short_url.description
        updated_short_url = storage.update_partial(
            short_url=self.short_url,
            short_url_in=short_url_partial_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_partial_update.description,
            updated_short_url.description,
        )


class ShortUrlStorageGetShortUrlsTestCase(TestCase):
    SHORT_URLS_COUNT = 3
    short_urls: ClassVar[list[ShortUrl]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.short_urls = [create_short_url() for _ in range(cls.SHORT_URLS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for short_url in cls.short_urls:
            storage.delete(short_url)

    def test_get_list(self) -> None:
        short_urls = storage.get()
        expected_slugs = {su.slug for su in self.short_urls}
        slugs = {su.slug for su in short_urls}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_by_slug(self) -> None:
        for short_url in self.short_urls:
            with self.subTest(
                slug=short_url.slug,
                msg=f"Validate can be slug {short_url.slug!r}",
            ):
                db_short_url = storage.get_by_slug(short_url.slug)
                self.assertEqual(
                    short_url,
                    db_short_url,
                )


def test_create_or_raise_if_exists(short_url: ShortUrl) -> None:
    short_url_in = ShortUrlCreate(**short_url.model_dump())
    with pytest.raises(
        ShortUrlAlreadyExistsError,
        match=short_url_in.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(short_url_in)

    assert exc_info.value.args[0] == short_url_in.slug
