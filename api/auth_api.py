from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    """Класс для работы с аутентификацией."""

    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)  # ✅ Правильно!
        # self.base_url уже есть в CustomRequester!

    def register_user(self, user_data, expected_status=201):
        """Регистрация пользователя."""
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, email, password, expected_status=200):  # ✅ email + password!
        """Авторизация пользователя."""
        login_data = {"email": email, "password": password}  # ✅ Создаём dict!
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        login_data = {"email": user_creds[0], "password": user_creds[1]}
        response = self.login_user(login_data)  # Внутри используй dict
        # ... остальной код
