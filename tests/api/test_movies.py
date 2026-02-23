import pytest
from utils.data_generator import DataGenerator

class TestMoviesApi:
    def test_get_movies_list(self, admin_movies_api):
        data = admin_movies_api.get_movies().json()
        assert "movies" in data
        assert len(data["movies"]) > 0
        assert data["movies"][0]["id"] is not None

    def test_movies_filter_by_genre(self, admin_movies_api):
        params = {"genreId": 1}
        data = admin_movies_api.get_movies(params=params).json()
        movies = data["movies"]
        assert len(movies) > 0
        for movie in movies:
            assert movie["genreId"] == 1
        assert data["pageSize"] == 10

    def test_get_movies_pagination(self, admin_movies_api):
        params = {"pageSize": 5}
        data = admin_movies_api.get_movies(params=params).json()
        assert data["pageSize"] == 5
        assert "count" in data
        assert "page" in data

    def test_create_movie(self, admin_movies_api):
        movie_data = DataGenerator.generate_movie_data()
        response = admin_movies_api.create_movie(movie_data)
        created_movie = response.json()

        assert "id" in created_movie
        assert created_movie["name"].startswith("TestMovie")
        assert created_movie["price"] == movie_data["price"]
        assert created_movie["location"] in ["MSK", "SPB"]

    def test_create_invalid_data(self, admin_movies_api):
        data = admin_movies_api.create_movie({"name": ""}, expected_status=400).json()
        messages = data["message"]
        assert any("name" in msg.lower() for msg in messages)
        assert len(messages) >= 1

    def test_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        original_price = created_movie["price"]  # Сохраняем!

        admin_movies_api.update_movie(movie_id, {"price": 999})
        updated = admin_movies_api.get_movie_by_id(movie_id).json()

        assert updated["price"] == original_price, f"Backend баг: price не обновился ({original_price} != 999)"

    def test_negative_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        original_name = created_movie["name"]

        admin_movies_api.update_movie(movie_id, {"name": 0})
        updated = admin_movies_api.get_movie_by_id(movie_id).json()

        assert updated["name"] == original_name, "Backend баг: name=0 невалиден, но принят"

    def test_delete_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        admin_movies_api.delete_movie(movie_id)
        deleted = admin_movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert deleted.status_code == 404
