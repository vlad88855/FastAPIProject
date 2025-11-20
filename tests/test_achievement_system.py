import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM
from service.AchievementHandlers import ReviewCountHandler, GenreMasterHandler
from service.AchievementService import AchievementService

class TestAchievementSystem(unittest.TestCase):

    def test_review_count_handler(self):
        handler = ReviewCountHandler()
        mock_db = MagicMock(spec=Session)
        
        # Mock count return value
        mock_db.query.return_value.filter.return_value.scalar.return_value = 5
        
        self.assertTrue(handler.check(1, {"threshold": 5}, mock_db))
        self.assertFalse(handler.check(1, {"threshold": 6}, mock_db))

    def test_genre_master_handler(self):
        handler = GenreMasterHandler()
        mock_db = MagicMock(spec=Session)
        
        # Mock count return value
        mock_db.query.return_value.join.return_value.filter.return_value.scalar.return_value = 5
        
        self.assertTrue(handler.check(1, {"genre": "Horror", "threshold": 5}, mock_db))
        self.assertFalse(handler.check(1, {"genre": "Horror", "threshold": 6}, mock_db))

    def test_achievement_service(self):
        mock_db = MagicMock(spec=Session)
        service = AchievementService(mock_db)
        
        # Mock achievements
        ach1 = AchievementORM(id=1, name="Test", condition_type="COUNT_REVIEWS", condition_params={"threshold": 5})
        mock_db.query.return_value.all.return_value = [ach1]
        
        # Mock user existing achievements (empty)
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Mock handler check to return True
        with unittest.mock.patch("service.AchievementHandlers.ReviewCountHandler.check", return_value=True):
            new_achievements = service.check_new_achievements(1)
            self.assertEqual(len(new_achievements), 1)
            self.assertEqual(new_achievements[0].name, "Test")

if __name__ == "__main__":
    unittest.main()
