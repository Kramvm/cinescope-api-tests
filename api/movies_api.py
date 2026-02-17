import uuid


class MoviesApi:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.endpoint = "/movies"

    def _send_request(self, method, endpoint, data=None, expected_status=200):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data)
        if response.status_code != expected_status:
            print(f"⚠️ Status {response.status_code} != expected {expected_status}")
        return response

    def get_movies(self, expected_status=200):
        return self._send_request("GET", self.endpoint, expected_status=expected_status)

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self._send_request("GET", f"{self.endpoint}/{movie_id}", expected_status=expected_status)

    def create_movie(self, movie_data=None, expected_status=201):
        if movie_data is None:
            movie_data = {
                "name": f"Test_{str(uuid.uuid4())[:8]}",
                "price": 100,
                "description": "Autotest movie",
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
        return self._send_request("POST", self.endpoint, movie_data, expected_status)

    def delete_movie(self, movie_id, expected_status=200):
        """⚠️ Этот метод не работает в API"""
        return self._send_request("DELETE", f"{self.endpoint}/{movie_id}", expected_status=expected_status)
