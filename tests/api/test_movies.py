import pytest
import allure
from utils.data_generator import DataGenerator
from models.movie_models import MoviesListResponse

@allure.feature("Movies")
@pytest.mark.api
class TestMoviesApi:
    @pytest.mark.smoke
    @allure.story("Get movies")
    @allure.title("Получение списка фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movies_list(self, admin_movies_api):
        data = admin_movies_api.movies_api.get_movies().json()
        result = MoviesListResponse(**data)
        assert len(result.movies) > 0

    @pytest.mark.regression
    @allure.story("Movies filter")
    @allure.title("Получение фильма по фильру Генре")
    @allure.severity(allure.severity_level.NORMAL)
    def test_movies_filter_by_genre(self, admin_movies_api):
        params = {"genreId": 1}
        data = admin_movies_api.movies_api.get_movies(params=params).json()
        movies = data["movies"]
        assert len(movies) > 0
        for movie in movies:
            assert movie["genreId"] == 1

    @pytest.mark.regression
    @allure.story("Pagination")
    @allure.title("Работа пагинации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_pagination(self, admin_movies_api):
        params = {"pageSize": 5}
        data = admin_movies_api.movies_api.get_movies(params=params).json()
        assert data["pageSize"] == 5
        assert "count" in data
        assert "page" in data

    @pytest.mark.smoke
    @allure.story("Create movie")
    @allure.title("Создание фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movie(self, created_movie, db_helper):
        assert "id" in created_movie
        assert created_movie["name"].startswith("TestMovie")
        assert created_movie["price"] > 0  # Дополнительная проверка
        assert created_movie["location"] in ["MSK", "SPB"]
        assert db_helper.get_movie_by_id(created_movie["id"]).name == created_movie["name"]

    @pytest.mark.regression
    @allure.story("Create movie")
    @allure.title("Создать невалидный фильм")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_invalid_data(self, admin_movies_api):
        data = admin_movies_api.movies_api.create_movie({"name": ""}, expected_status=400).json()
        messages = data["message"]
        assert any("name" in msg.lower() for msg in messages)
        assert len(messages) >= 1

    @pytest.mark.smoke
    @allure.story("Update movie")
    @allure.title("Обновление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        admin_movies_api.movies_api.update_movie(movie_id, {"price": 999})
        updated = admin_movies_api.movies_api.get_movie_by_id(movie_id).json()
        assert updated["price"] == 999

    @pytest.mark.regression
    @allure.story("Update movie")
    @allure.title("Обновление фильма негативный")
    @allure.severity(allure.severity_level.NORMAL)
    def test_negative_update_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        response = admin_movies_api.movies_api.update_movie(movie_id, {"name": 0}, expected_status=400)
        assert response.status_code == 400, "name=0 должен отклонить"

    @pytest.mark.smoke
    @allure.story("Delete movie")
    @allure.title("Удаление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movie(self, admin_movies_api, created_movie):
        movie_id = created_movie["id"]
        response = admin_movies_api.movies_api.delete_movie(movie_id)
        assert response.status_code == 200, "DELETE должен вернуть 200"
        deleted_movie = response.json()
        assert deleted_movie["id"] == movie_id, "ID должен совпадать"
        assert len(deleted_movie["reviews"]) == 0, "Reviews пустые"

    @pytest.mark.parametrize("filter_type,param_value,expected_count", [
        ("minPrice", 100, ">5"),
        ("maxPrice", 200, "<50"),
        ("location", "SPB", "exists"),
        ("genreId", 3, "exists"),
    ])
    @pytest.mark.regression
    @allure.story("Movie filter")
    @allure.title("Тестирование фильтра")
    @allure.severity(allure.severity_level.NORMAL)
    def test_movies_filter(self, admin_movies_api, filter_type, param_value, expected_count):
        response = admin_movies_api.movies_api.get_movies(params={filter_type: param_value})
        movies = response.json()["movies"]

        if expected_count == ">5": assert len(movies) > 5
        if expected_count == "<50": assert len(movies) < 50
        if expected_count == "exists": assert len(movies) > 0


@pytest.mark.api
@allure.feature("Movies")
class TestMoviesRoles:

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.story("Create movie")
    @allure.title("Создание фильма без прав")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_common_user(self, common_user):
        """Юзер с ролью USER не может создать фильм — ожидаем 403"""
        movie_data = DataGenerator.generate_movie_data()
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @pytest.mark.parametrize("role,expected_status", [
        ("super_admin", 200),
        ("common_user", 403),
    ])
    @pytest.mark.regression
    @pytest.mark.slow
    @allure.story("Delete movie")
    @allure.title("Удаление фильма без прав")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie_roles(self, role, expected_status, request, created_movie):
        """Только SUPER_ADMIN может удалить фильм"""
        user = request.getfixturevalue(role)
        user.api.movies_api.delete_movie(created_movie["id"], expected_status=expected_status)