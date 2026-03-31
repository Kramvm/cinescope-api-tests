import pytest

from models.base_models import RegisterUserResponse


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data, expected_status=201)
        user_response = RegisterUserResponse(**response.json())

        assert user_response.email == creation_user_data['email']
        assert user_response.fullName == creation_user_data['fullName']
        assert user_response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created = RegisterUserResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        by_id = RegisterUserResponse(**super_admin.api.user_api.get_user(created.id).json())
        by_email = RegisterUserResponse(**super_admin.api.user_api.get_user(creation_user_data['email']).json())

        assert by_id == by_email, "Содержание ответов должно быть идентичным"
        assert by_id.email == creation_user_data['email']
        assert by_id.fullName == creation_user_data['fullName']
        assert by_id.verified is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    def test_create_user_common_user(self, common_user, creation_user_data):
        common_user.api.user_api.create_user(creation_user_data, expected_status=403)

    @pytest.mark.slow
    def test_create_user_admin(self, super_admin, creation_user_data):
        super_admin.api.user_api.create_user(creation_user_data, expected_status=201)
