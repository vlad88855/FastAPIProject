import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from service.AchievementHandlers import ReviewCountHandler, GenreMasterHandler

class TestAchievementHandlers(unittest.TestCase):

    def test_review_count_handler_success(self):
        # Arrange
        handler = ReviewCountHandler()
        mock_db = MagicMock(spec=Session)
        user_id = 1
        params = {"threshold": 5}
        
        # Mock the query chain: db.query().filter().scalar() -> 5
        mock_db.query.return_value.filter.return_value.scalar.return_value = 5
        
        # Act
        result = handler.check(user_id, params, mock_db)
        
        # Assert
        self.assertTrue(result)

    def test_review_count_handler_failure(self):
        # Arrange
        handler = ReviewCountHandler()
        mock_db = MagicMock(spec=Session)
        user_id = 1
        params = {"threshold": 6}
        
        # Mock the query chain: db.query().filter().scalar() -> 5
        mock_db.query.return_value.filter.return_value.scalar.return_value = 5
        
        # Act
        result = handler.check(user_id, params, mock_db)
        
        # Assert
        self.assertFalse(result)

    def test_genre_master_handler_success(self):
        # Arrange
        handler = GenreMasterHandler()
        mock_db = MagicMock(spec=Session)
        user_id = 1
        params = {"genre": "Horror", "threshold": 5}
        
        # Mock the query chain: db.query().join().filter().scalar() -> 5
        mock_db.query.return_value.join.return_value.filter.return_value.scalar.return_value = 5
        
        # Act
        result = handler.check(user_id, params, mock_db)
        
        # Assert
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
