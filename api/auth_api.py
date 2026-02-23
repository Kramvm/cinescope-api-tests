from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):

    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def register_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, email, password, expected_status=200):
        login_data = {"email": email, "password": password}
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        email, password = user_creds
        response = self.login_user(email, password)
        if response.status_code == 200:
            token = response.json()["accessToken"]
            self.session.headers["Authorization"] = f"Bearer {token}"
        return response