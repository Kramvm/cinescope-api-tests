import pytest
import requests
from sqlalchemy.orm import Session
from constants import BASE_URL
from entities.user import User
from resources.user_creds import SuperAdminCreds, AdminCreds
from roles import Roles
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from db_models.base_models import TestUser
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session, BASE_URL)


@pytest.fixture(scope="session")
def admin_movies_api(api_manager):
    response = api_manager.auth_api.login_user("api1@gmail.com", "asdqwe123Q", expected_status=200)
    token = response.json()["accessToken"]
    api_manager.session.headers["Authorization"] = f"Bearer {token}"
    return api_manager


@pytest.fixture(scope="function")
def created_movie(admin_movies_api):
    movie_data = DataGenerator.generate_movie_data()
    response = admin_movies_api.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie
    try:
        admin_movies_api.movies_api.delete_movie(movie["id"])
    except AssertionError as e:
        if "404" not in str(e):
            raise  # Только НЕ 404 ошибки пробрасываем

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user: TestUser):
    api_manager.auth_api.register_user(test_user)
    yield test_user
    try:
        api_manager.user_api.delete_user(test_user.email, expected_status=204)
    except AssertionError:
        pass  # 404 = OK, пользователь уже удалён

@pytest.fixture(scope="function")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        api_manager = ApiManager(session, BASE_URL)
        user_pool.append(api_manager)
        return api_manager

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, [Roles.SUPER_ADMIN.value], new_session)

    response = super_admin.api.auth_api.authenticate(super_admin.creds)
    token = response.json()["accessToken"]
    new_session.session.headers["Authorization"] = f"Bearer {token}"

    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser):
    data = test_user.model_dump(mode="json")
    data.update({
        "verified": True,
        "banned": False,
        "roles": [Roles.USER.value]
    })
    return data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session):
    new_session = user_session()

    admin = User(AdminCreds.USERNAME, AdminCreds.PASSWORD, [Roles.ADMIN.value], new_session)

    response = admin.api.auth_api.authenticate(admin.creds)
    token = response.json()["accessToken"]
    new_session.session.headers["Authorization"] = f"Bearer {token}"

    return admin


@pytest.fixture(scope="module")
def db_session() -> Session:
    session = get_db_session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    yield DBHelper(db_session)
    db_session.rollback()


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)