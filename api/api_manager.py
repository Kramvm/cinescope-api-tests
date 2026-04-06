from api.auth_api import AuthAPI
from api.user_api import UserApi
from api.movies_api import MoviesApi
from constants import MOVIES_BASE_URL
from custom_requester.custom_requester import CustomRequester

class ApiManager:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.requester = CustomRequester(session, base_url)
        self.auth_api = AuthAPI(session, base_url)
        self.user_api = UserApi(session)
        self.movies_api = MoviesApi(session, MOVIES_BASE_URL)

    def close_session(self):
        self.session.close()