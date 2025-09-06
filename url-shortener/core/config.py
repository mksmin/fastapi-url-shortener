import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

USERS_DB: dict[str, str] = {
    "sam": "password",
    "bob": "qwerty",
}


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    tokens: int = 1
    users: int = 2
    urls: int = 3


class RedisCollectionsNamesConfig(BaseModel):
    tokens_set: str = "tokens"
    short_urls_hash: str = "short_urls"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDatabaseConfig = RedisDatabaseConfig()
    collections_names: RedisCollectionsNamesConfig = RedisCollectionsNamesConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
