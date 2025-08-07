import logging
from pydantic import BaseModel, AnyHttpUrl, ValidationError
from redis import Redis

from core import config
from core.config import SHORT_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

redis_short_urls = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_URLS,
    decode_responses=True,
)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.info("Short urls storage file doesn't exist.")
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlsStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error")
            return

        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )
        log.warning("Recovered data from storage file.")

    def get(self) -> list[ShortUrl]:
        return [
            ShortUrl.model_validate_json(value)
            for value in redis_short_urls.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis_short_urls.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(data)

    def create(self, short_url: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url.model_dump(),
        )
        redis_short_urls.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        log.info("Created short url")
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:

        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        return short_url


storage = ShortUrlsStorage()
