
from faker import Faker
import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, MOVIES_BASE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
faker = Faker()

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
    api_manager.auth_api.authenticate(("api1@gmail.com", "asdqwe123Q"))
    return api_manager.movies_api

@pytest.fixture(scope="function")
def created_movie(admin_movies_api):
    movie_data = DataGenerator.generate_movie_data()
    response = admin_movies_api.create_movie(movie_data)
    movie = response.json()

    yield movie

    admin_movies_api.delete_movie(movie["id"])
