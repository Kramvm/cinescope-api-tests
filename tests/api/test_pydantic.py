from models.pydan import RegistrationUserModel


def test_validate_test_user(test_user):
    model = RegistrationUserModel(**test_user.model_dump())


def test_validate_creation_user_data(creation_user_data):
    model = RegistrationUserModel(**creation_user_data)
