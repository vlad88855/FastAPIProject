import unittest
from unittest.mock import MagicMock
from service.MovieService import MovieService
from repository.MovieRepository import MovieRepository
from repository.UserRatingRepository import UserRatingRepository
from service.CacheService import CacheService
from service.ConfigService import ConfigService
from model.DTOs.MovieDTO import MovieCreate, MovieOut, MovieGenre, MovieUpdate
from model.MovieORM import MovieORM

class TestMovieService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock(spec=MovieRepository)
        self.mock_rating_repo = MagicMock(spec=UserRatingRepository)
        self.mock_cache = MagicMock(spec=CacheService)
        self.mock_config = MagicMock(spec=ConfigService)
        
        self.service = MovieService(
            self.mock_repo, 
            self.mock_rating_repo, 
            self.mock_cache, 
            self.mock_config
        )

    # --- 1. Single Entity CRUD ---

    def test_create_success(self):
        # Arrange
        dto = MovieCreate(title="Test Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA)
        movie_orm = MovieORM(id=1, title="Test Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.create_movie.return_value = movie_orm

        # Act
        result = self.service.create_movie(dto)

        # Assert
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Test Movie")
        self.mock_repo.create_movie.assert_called_once_with(dto)

    def test_get_success(self):
        # Arrange
        movie_id = 1
        movie_orm = MovieORM(id=movie_id, title="Test", description="D", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.get_movie.return_value = movie_orm

        # Act
        result = self.service.get_movie(movie_id)

        # Assert
        self.assertEqual(result.id, movie_id)
        self.mock_repo.get_movie.assert_called_once_with(movie_id)

    def test_update_success(self):
        # Arrange
        movie_id = 1
        dto = MovieUpdate(title="Updated Title")
        movie_orm = MovieORM(id=1, title="Updated Title", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.update_movie.return_value = movie_orm

        # Act
        result = self.service.update_movie(movie_id, dto)

        # Assert
        self.assertEqual(result.title, "Updated Title")
        self.mock_repo.update_movie.assert_called_once_with(movie_id, dto)

    def test_delete_success(self):
        # Arrange
        movie_id = 1

        # Act
        self.service.delete_movie(movie_id)

        # Assert
        self.mock_repo.delete_movie.assert_called_once_with(movie_id)

    def test_create_duplicate(self):
        # Arrange
        dto = MovieCreate(title="Test Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA)
        self.mock_repo.create_movie.side_effect = Exception("Duplicate entry")

        # Act & Assert
        with self.assertRaises(Exception): # Expecting 409 or similar
             self.service.create_movie(dto)

    def test_get_not_found(self):
        # Arrange
        movie_id = 999
        self.mock_repo.get_movie.return_value = None

        # Act & Assert
        with self.assertRaises(Exception): # Expecting 404
             self.service.get_movie(movie_id)

    def test_update_not_found(self):
        # Arrange
        movie_id = 999
        dto = MovieUpdate(title="Updated")
        self.mock_repo.update_movie.return_value = None

        # Act & Assert
        with self.assertRaises(Exception): # Expecting 404
             self.service.update_movie(movie_id, dto)

    def test_delete_not_found(self):
        # Arrange
        movie_id = 999
        self.mock_repo.get_movie.return_value = None
        
        # Act & Assert
        with self.assertRaises(Exception): # Expecting 404
            self.service.delete_movie(movie_id)

    # --- 2. Collections & Pagination ---

    def test_get_list_success(self):
        # Arrange
        self.mock_config.get.return_value = 10
        self.mock_cache.get.return_value = None
        movie_orm = MovieORM(id=1, title="DB Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.get_paginated.return_value = [movie_orm]

        # Act
        result = self.service.get_all_movies(skip=0, limit=None)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "DB Movie")

    def test_get_list_empty(self):
        # Arrange
        self.mock_config.get.return_value = 10
        self.mock_cache.get.return_value = None
        self.mock_repo.get_paginated.return_value = []

        # Act
        result = self.service.get_all_movies(skip=0, limit=None)

        # Assert
        self.assertEqual(result, [])

    def test_get_list_pagination(self):
        # Arrange
        self.mock_cache.get.return_value = None
        self.mock_repo.get_paginated.return_value = []
        
        # Act
        self.service.get_all_movies(skip=5, limit=20)

        # Assert
        self.mock_repo.get_paginated.assert_called_once_with(5, 20)

    # --- 3. Unique Logic (Caching, Ratings, Genres) ---

    def test_get_all_movies_cache_hit(self):
        # Arrange
        cache_key = "movies_skip_0_limit_10_genre_None"
        cached_data = [MovieOut(id=1, title="Cached Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)]
        self.mock_config.get.return_value = 10
        self.mock_cache.get.return_value = cached_data

        # Act
        result = self.service.get_all_movies(skip=0, limit=None)

        # Assert
        self.assertEqual(result, cached_data)
        self.mock_repo.get_paginated.assert_not_called()

    def test_get_all_movies_cache_miss(self):
        # Arrange
        self.mock_config.get.return_value = 10
        self.mock_cache.get.return_value = None
        movie_orm = MovieORM(id=1, title="DB Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.get_paginated.return_value = [movie_orm]

        # Act
        result = self.service.get_all_movies(skip=0, limit=None)

        # Assert
        self.assertEqual(len(result), 1)
        self.mock_repo.get_paginated.assert_called_once()
        self.mock_cache.set.assert_called_once()

    def test_create_movie_invalidates_cache(self):
        # Arrange
        dto = MovieCreate(title="New", description="D", year=2023, genre=MovieGenre.DRAMA)
        self.mock_repo.create_movie.return_value = MovieORM(id=1, title="New", description="D", year=2023, genre=MovieGenre.DRAMA, view_count=0)

        # Act
        self.service.create_movie(dto)

        # Assert
        self.mock_cache.clear_all_starting_with.assert_called_once_with("movies_")

    def test_update_movie_invalidates_cache(self):
        # Arrange
        movie_id = 1
        dto = MovieUpdate(title="Updated")
        self.mock_repo.update_movie.return_value = MovieORM(id=1, title="Updated", description="D", year=2023, genre=MovieGenre.DRAMA, view_count=0)

        # Act
        self.service.update_movie(movie_id, dto)

        # Assert
        self.mock_cache.clear_all_starting_with.assert_called_once_with("movies_")

    def test_get_movie_rating_none(self):
        # Arrange
        movie_id = 1
        self.mock_repo.get_movie.return_value = MovieORM(id=1, title="Test", description="D", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_rating_repo.get_average_rating.return_value = None

        # Act
        result = self.service.get_movie_rating(movie_id)

        # Assert
        # Should return 0.0, not None
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_get_all_movies_by_genre(self):
        # Arrange
        genre = MovieGenre.DRAMA
        self.mock_config.get.return_value = 10
        self.mock_cache.get.return_value = None
        movie_orm = MovieORM(id=1, title="Drama Movie", description="Desc", year=2023, genre=MovieGenre.DRAMA, view_count=0)
        self.mock_repo.get_by_genre.return_value = [movie_orm]

        # Act
        result = self.service.get_all_movies(skip=0, limit=None, genre=genre)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].genre, MovieGenre.DRAMA)
        self.mock_repo.get_by_genre.assert_called_once_with(genre, 0, 10)

if __name__ == '__main__':
    unittest.main()
