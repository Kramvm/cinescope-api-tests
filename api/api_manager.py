from api.auth_api import AuthAPI
from api.user_api import UserAPI
from constants import MOVIES_BASE_URL
from custom_requester.custom_requester import CustomRequester


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.requester = CustomRequester(session, base_url)  # ← НОВОЕ!
        self.auth_api = AuthAPI(session, base_url)
        self.user_api = UserAPI(session, base_url)

    @property
    def movies(self):
        """Movies API"""
        from .movies_api import MoviesApi  # ← уже есть
        return MoviesApi(self.session, MOVIES_BASE_URL)  # ← ИЗМЕНИ base_url!




