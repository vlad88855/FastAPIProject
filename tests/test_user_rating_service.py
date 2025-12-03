import unittest
from unittest.mock import MagicMock
from datetime import datetime
from service.UserRatingService import UserRatingService
from repository.UserRatingRepository import UserRatingRepository
from repository.UserRepository import UserRepository
from repository.MovieRepository import MovieRepository
from service.AchievementService import AchievementService
from model.DTOs.UserRatingDTO import UserRatingCreate, UserRatingOut, UserRatingUpdate
from model.UserRatingORM import UserRatingORM
from model.MovieORM import MovieORM
from repository.exceptions import UserRatingExistsException

class TestUserRatingService(unittest.TestCase):

    def setUp(self):
        self.mock_rating_repo = MagicMock(spec=UserRatingRepository)
        self.mock_user_repo = MagicMock(spec=UserRepository)
        self.mock_movie_repo = MagicMock(spec=MovieRepository)
        self.mock_achievement_service = MagicMock(spec=AchievementService)
        
        self.service = UserRatingService(
            self.mock_rating_repo, 
            self.mock_user_repo, 
            self.mock_movie_repo, 
            self.mock_achievement_service
        )

    # --- CRUD ---

    def test_create_success(self):
        # Arrange
        dto = UserRatingCreate(user_id=1, movie_id=1, rating=10, comment="Great!")
        rating_orm = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=10, 
            comment="Great!", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        
        self.mock_user_repo.get_user.return_value = MagicMock()
        self.mock_movie_repo.get_movie.return_value = MovieORM(id=1, view_count=0)
        self.mock_rating_repo.find_rating_by_user_movie.return_value = None
        self.mock_rating_repo.create_rating.return_value = rating_orm
        self.mock_rating_repo.get_average_rating.return_value = 10.0

        # Act
        result = self.service.create_rating(dto)

        # Assert
        self.assertEqual(result.id, 1)
        self.assertEqual(result.rating, 10)
        self.mock_rating_repo.create_rating.assert_called_once_with(dto)

    def test_get_success(self):
        # Arrange
        rating_id = 1
        rating_orm = UserRatingORM(
            id=rating_id, user_id=1, movie_id=1, rating=8, 
            comment="Good", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.get_rating.return_value = rating_orm

        # Act
        result = self.service.get_rating(rating_id)

        # Assert
        self.assertEqual(result.id, rating_id)
        self.mock_rating_repo.get_rating.assert_called_once_with(rating_id)

    def test_update_success(self):
        # Arrange
        rating_id = 1
        dto = UserRatingUpdate(rating=9)
        rating_orm = UserRatingORM(
            id=rating_id, user_id=1, movie_id=1, rating=9, 
            comment="Good", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.update_rating.return_value = rating_orm
        self.mock_rating_repo.get_rating.return_value = rating_orm

        # Act
        result = self.service.update_rating(rating_id, dto)

        # Assert
        self.assertEqual(result.rating, 9)
        self.mock_rating_repo.update_rating.assert_called_once_with(rating_id, dto)

    def test_delete_success(self):
        # Arrange
        rating_id = 1

        # Act
        self.service.delete_rating(rating_id)

        # Assert
        self.mock_rating_repo.delete_rating.assert_called_once_with(rating_id)

    def test_create_duplicate(self):
        # Arrange
        dto = UserRatingCreate(user_id=1, movie_id=1, rating=10)
        self.mock_user_repo.get_user.return_value = MagicMock()
        self.mock_movie_repo.get_movie.return_value = MagicMock()
        self.mock_rating_repo.find_rating_by_user_movie.return_value = MagicMock()

        # Act & Assert
        with self.assertRaises(UserRatingExistsException):
            self.service.create_rating(dto)

    def test_get_not_found(self):
        # Arrange
        rating_id = 999
        self.mock_rating_repo.get_rating.return_value = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.service.get_rating(rating_id)

    def test_update_not_found(self):
        # Arrange
        rating_id = 999
        dto = UserRatingUpdate(rating=5)
        self.mock_rating_repo.get_rating.return_value = None
        self.mock_rating_repo.update_rating.return_value = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.service.update_rating(rating_id, dto)

    def test_delete_not_found(self):
        # Arrange
        rating_id = 999
        self.mock_rating_repo.get_rating.return_value = None
        
        # Act & Assert
        with self.assertRaises(Exception):
            self.service.delete_rating(rating_id)

    # --- Collections ---

    def test_get_list_success(self):
        # Arrange
        rating_orm = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=8, 
            comment="Good", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.get_all_ratings.return_value = [rating_orm]

        # Act
        result = self.service.get_all_ratings()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].rating, 8)

    def test_get_list_empty(self):
        # Arrange
        self.mock_rating_repo.get_all_ratings.return_value = []

        # Act
        result = self.service.get_all_ratings()

        # Assert
        self.assertEqual(result, [])

    # --- Logic ---

    def test_create_rating_updates_average(self):
        # Arrange
        dto = UserRatingCreate(user_id=1, movie_id=1, rating=10)
        self.mock_user_repo.get_user.return_value = MagicMock()
        self.mock_movie_repo.get_movie.return_value = MovieORM(id=1, view_count=0)
        self.mock_rating_repo.find_rating_by_user_movie.return_value = None
        self.mock_rating_repo.create_rating.return_value = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=10, 
            comment="", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.get_average_rating.return_value = 9.5

        # Act
        self.service.create_rating(dto)

        # Assert
        self.mock_movie_repo.update_average_rating.assert_called_once_with(1, 9.5)

    def test_update_rating_updates_average(self):
        # Arrange
        rating_id = 1
        dto = UserRatingUpdate(rating=5)
        
        existing_rating = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=10, 
            comment="", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.get_rating.return_value = existing_rating
        
        updated_rating = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=5, 
            comment="", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.update_rating.return_value = updated_rating
        self.mock_rating_repo.get_average_rating.return_value = 7.5

        # Act
        self.service.update_rating(rating_id, dto)

        # Assert
        self.mock_movie_repo.update_average_rating.assert_called_once_with(1, 7.5)

    def test_delete_rating_updates_average(self):
        # Arrange
        rating_id = 1
        existing_rating = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=10, 
            comment="", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )
        self.mock_rating_repo.get_rating.return_value = existing_rating
        self.mock_rating_repo.get_average_rating.return_value = 8.0

        # Act
        self.service.delete_rating(rating_id)

        # Assert
        self.mock_movie_repo.update_average_rating.assert_called_once_with(1, 8.0)

    def test_create_rating_triggers_achievements(self):
        # Arrange
        dto = UserRatingCreate(user_id=1, movie_id=1, rating=10)
        self.mock_user_repo.get_user.return_value = MagicMock()
        self.mock_movie_repo.get_movie.return_value = MovieORM(id=1, view_count=0)
        self.mock_rating_repo.find_rating_by_user_movie.return_value = None
        self.mock_rating_repo.create_rating.return_value = UserRatingORM(
            id=1, user_id=1, movie_id=1, rating=10, 
            comment="", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )

        # Act
        self.service.create_rating(dto)

        # Assert
        self.mock_achievement_service.check_new_achievements.assert_called_once_with(1)

    def test_create_rating_user_not_found(self):
        # Arrange
        dto = UserRatingCreate(user_id=999, movie_id=1, rating=10)
        self.mock_user_repo.get_user.return_value = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.service.create_rating(dto)

    def test_create_rating_movie_not_found(self):
        # Arrange
        dto = UserRatingCreate(user_id=1, movie_id=999, rating=10)
        self.mock_user_repo.get_user.return_value = MagicMock()
        self.mock_movie_repo.get_movie.return_value = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.service.create_rating(dto)

if __name__ == '__main__':
    unittest.main()
