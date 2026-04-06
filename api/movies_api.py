from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_ENDPOINT

class MoviesApi(CustomRequester):

    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def get_movies(self, params = None, expected_status=200):
        return self.send_request("GET", MOVIES_ENDPOINT, params=params, expected_status=expected_status)

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request("GET", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request("POST", MOVIES_ENDPOINT, data=movie_data, expected_status=expected_status)

    def update_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}", data=movie_data, expected_status=expected_status)

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request("DELETE", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status)
