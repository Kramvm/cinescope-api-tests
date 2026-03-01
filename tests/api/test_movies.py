
class TestMoviesApi:
    def test_get_movies_list(self, admin_movies_api):
        data = admin_movies_api.movies_api.get_movies().json()
        assert "movies" in data
        assert len(data["movies"]) > 0
        assert data["movies"][0]["id"] is not None

    def test_movies_filter_by_genre(self, admin_movies_api):
        params = {"genreId": 1}
        data = admin_movies_api.movies_api.get_movies(params=params).json()
        movies = data["movies"]
        assert len(movies) > 0
        for movie in movies:
            assert movie["genreId"] == 1

    def test_get_movies_pagination(self, admin_movies_api):
        params = {"pageSize": 5}
        data = admin_movies_api.movies_api.get_movies(params=params).json()
        assert data["pageSize"] == 5
        assert "count" in data
        assert "page" in data

    def test_create_movie(self, created_movie):
        assert "id" in created_movie
        assert created_movie["name"].startswith("TestMovie")
        assert created_movie["price"] > 0  # Дополнительная проверка
        assert created_movie["location"] in ["MSK", "SPB"]

    def test_create_invalid_data(self, admin_movies_api):
        data = admin_movies_api.movies_api.create_movie({"name": ""}, expected_status=400).json()
        messages = data["message"]
        assert any("name" in msg.lower() for msg in messages)
        assert len(messages) >= 1

    def test_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        admin_movies_api.movies_api.update_movie(movie_id, {"price": 999})
        updated = admin_movies_api.movies_api.get_movie_by_id(movie_id).json()
        assert updated["price"] == 999

    def test_negative_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        response = admin_movies_api.movies_api.update_movie(movie_id, {"name": 0}, expected_status=400)
        assert response.status_code == 400, "name=0 должен отклонить"

    def test_delete_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        admin_movies_api.movies_api.delete_movie(movie_id)
        deleted = admin_movies_api.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert deleted.status_code == 404
