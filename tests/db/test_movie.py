import pytest

class TestMovieDB:

    def test_movie_exists_in_db(self, created_movie, db_helper):
        movie_id = created_movie["id"]
        movie = db_helper.get_movie_by_id(movie_id)
        assert movie is not None

    def test_movie_validate_name(self, created_movie, db_helper):
        movie_name = created_movie["name"]
        movie_name_bd = db_helper.get_movie_by_name(movie_name)
        assert movie_name == movie_name_bd.name

    def test_movie_delete(self, admin_movies_api,db_helper, created_movie):
        movie_id = created_movie["id"]
        admin_movies_api.movies_api.delete_movie(movie_id)
        movie_db = db_helper.get_movie_by_id(movie_id)
        assert movie_db is None

