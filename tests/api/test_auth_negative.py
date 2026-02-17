import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:
    def test_login_wrong_password(self, api_manager, test_user):
        """Негатив: неверный пароль для существующего пользователя"""
        response = api_manager.auth_api.login_user(
            email=test_user["email"],
            password="00010001",
            expected_status = 401  # ✅ Скажи что ждём 401!
        )

    def test_login_wrong_email(self, api_manager, test_user):
        """Негатив: неверный email для существующего пользователя"""

        response = api_manager.auth_api.login_user(
            email="belyi",
            password=test_user["password"],
            expected_status=401  # ✅ Скажи что ждём 401!
        )

    def test_login_empty_body(self, api_manager, test_user):
        """Негатив: пустое тело запроса"""

        response = api_manager.auth_api.login_user(
            email="",
            password="",
            expected_status=401)