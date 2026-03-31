import pytest

from api.api_manager import ApiManager
from models.base_models import TestUser, RegisterUserResponse


class TestAuthAPI:
    @pytest.mark.slow
    def test_register_user(self, api_manager: ApiManager, test_user: TestUser):
        response = api_manager.auth_api.register_user(test_user, expected_status=201)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user: TestUser):
        response = api_manager.auth_api.login_user(
            email=registered_user.email,
            password=registered_user.password,
            expected_status=200
        )
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user.email
