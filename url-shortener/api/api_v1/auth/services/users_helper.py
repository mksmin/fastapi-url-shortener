from abc import ABC, abstractmethod


class UsersHelper(ABC):
    """
    Что мне нужно от обертки:
    - Получение пароля по username
    - Совпадает ли пароль с переданным

    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному username находит пароль.

        Возращает пароль если есть

        :param username: имя пользователя
        :return: пароль по пользователю, если найден
        """

    @classmethod
    def check_passwords_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Проверить совпадают ли пароли
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверить валидность пароля.

        :param username: чей пароль проверить
        :param password: переданный пароль. Сверить с тем, что в ЬД
        :return: True если совпадает, иначе False
        """

        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_match(
            password1=db_password,
            password2=password,
        )
