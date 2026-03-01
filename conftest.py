import pytest
import requests
from constants import BASE_URL
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager

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
    response = api_manager.auth_api.login_user("api1@gmail.com", "asdqwe123Q", expected_status=201)
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
    except AssertionError:
        pass

@pytest.fixture
def test_user():
    import uuid
    short_uuid = uuid.uuid4().hex[:6]
    return {
        "email": f"test{short_uuid}@ex.com",
        "fullName": "Test User",
        "password": "Test1234",
        "passwordRepeat": "Test1234"
    }


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    try:
        api_manager.auth_api.delete_user(test_user["email"])
    except:
        pass

    api_manager.auth_api.register_user(test_user)
    yield test_user

    try:
        api_manager.auth_api.delete_user(test_user["email"])
    except:
        pass


