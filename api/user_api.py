from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL


class UserApi(CustomRequester):
    USER_BASE_URL = BASE_URL

    def __init__(self, session: object) -> None:
        self.session = session
        super().__init__(session, self.USER_BASE_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request("GET", f"user/{user_locator}", expected_status=expected_status)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )