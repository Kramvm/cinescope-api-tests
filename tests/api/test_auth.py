import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """✅ Регистрация пользователя"""
        response = api_manager.auth_api.register_user(test_user, expected_status=201)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        """✅ Успешный логин"""
        response = api_manager.auth_api.login_user(
            email=registered_user["email"],
            password=registered_user["password"],
            expected_status=200
        )
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]
