import secrets
from abc import ABC, abstractmethod


class TokensHelper(ABC):
    """
    Что мне нужно от обертки:
    - Проверять наличие токена
    - Добавлять токен в хранилище
    - Сгенерировать и добавить токены
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Checks if token exists in redis
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token in storage
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(
        self,
    ) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
