import unittest
from unittest.mock import MagicMock
from datetime import datetime
from sqlalchemy.orm import Session
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM
from service.AchievementService import AchievementService

class TestViewAchievements(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.service = AchievementService(self.mock_db)
        self.user_id = 1
        self.now = datetime.now()

        # Mock Data
        self.ach1 = AchievementORM(id=1, name="Ach1", description="Desc1", condition_type="TYPE", condition_params={})
        self.ach2 = AchievementORM(id=2, name="Ach2", description="Desc2", condition_type="TYPE", condition_params={})
        
        self.ua1 = UserAchievementORM(user_id=self.user_id, achievement_id=1, earned_at=self.now)

    def test_get_user_achievements(self):
        # Mock query for user achievements
        # The query joins UserAchievementORM and AchievementORM
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [
            (self.ua1, self.ach1)
        ]

        result = self.service.get_user_achievements(self.user_id)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Ach1")
        self.assertEqual(result[0].earned_at, self.now)

    def test_get_achievements_status(self):
        # Mock query for all achievements
        self.mock_db.query.return_value.all.return_value = [self.ach1, self.ach2]
        
        # Mock query for user achievements (to build map)
        # Note: The service calls db.query(UserAchievementORM).filter(...).all()
        # We need to mock the chain correctly.
        # First call to query(AchievementORM) returns [ach1, ach2]
        # Second call to query(UserAchievementORM) returns [ua1]
        
        # We can use side_effect to return different values for consecutive calls
        def query_side_effect(model):
            mock_query = MagicMock()
            if model == AchievementORM:
                mock_query.all.return_value = [self.ach1, self.ach2]
            elif model == UserAchievementORM:
                mock_query.filter.return_value.all.return_value = [self.ua1]
            return mock_query

        self.mock_db.query.side_effect = query_side_effect

        result = self.service.get_achievements_status(self.user_id)
        
        self.assertEqual(len(result), 2)
        
        # Check Ach1 (Earned)
        ach1_status = next(r for r in result if r.id == 1)
        self.assertTrue(ach1_status.earned)
        self.assertEqual(ach1_status.earned_at, self.now)
        
        # Check Ach2 (Not Earned)
        ach2_status = next(r for r in result if r.id == 2)
        self.assertFalse(ach2_status.earned)
        self.assertIsNone(ach2_status.earned_at)

if __name__ == "__main__":
    unittest.main()
