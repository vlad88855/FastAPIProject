import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from service.AchievementService import AchievementService
from repository.AchievementRepository import AchievementRepository
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM
from service.AchievementHandlers import HandlerRegistry, BaseAchievementHandler

class TestAchievementService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock(spec=AchievementRepository)
        self.mock_db = MagicMock()
        self.service = AchievementService(self.mock_repo, self.mock_db)

    def test_check_new_achievements_success(self):
        # Arrange
        user_id = 1
        achievement = AchievementORM(
            id=1, 
            name="Test Achievement", 
            condition_type="TEST_TYPE", 
            condition_params={"threshold": 5}
        )
        self.mock_repo.get_all_achievements.return_value = [achievement]
        self.mock_repo.get_user_achievement_ids.return_value = set() # User has no achievements

        # Mock the handler
        mock_handler = MagicMock(spec=BaseAchievementHandler)
        mock_handler.check.return_value = True # Condition met
        
        with patch.object(HandlerRegistry, 'get_handler', return_value=mock_handler):
            # Act
            new_achievements = self.service.check_new_achievements(user_id)

            # Assert
            self.assertEqual(len(new_achievements), 1)
            self.assertEqual(new_achievements[0].name, "Test Achievement")
            self.mock_repo.add_user_achievement.assert_called_once_with(user_id, achievement.id)
            mock_handler.check.assert_called_once_with(user_id, achievement.condition_params, self.mock_db)

    def test_check_new_achievements_already_earned(self):
        # Arrange
        user_id = 1
        achievement = AchievementORM(id=1, name="Test Achievement", condition_type="TEST_TYPE", condition_params={})
        self.mock_repo.get_all_achievements.return_value = [achievement]
        self.mock_repo.get_user_achievement_ids.return_value = {1} # User already has this achievement

        # Act
        new_achievements = self.service.check_new_achievements(user_id)

        # Assert
        self.assertEqual(len(new_achievements), 0)
        self.mock_repo.add_user_achievement.assert_not_called()

    def test_check_new_achievements_condition_not_met(self):
        # Arrange
        user_id = 1
        achievement = AchievementORM(id=1, name="Test Achievement", condition_type="TEST_TYPE", condition_params={})
        self.mock_repo.get_all_achievements.return_value = [achievement]
        self.mock_repo.get_user_achievement_ids.return_value = set()

        mock_handler = MagicMock(spec=BaseAchievementHandler)
        mock_handler.check.return_value = False # Condition NOT met
        
        with patch.object(HandlerRegistry, 'get_handler', return_value=mock_handler):
            # Act
            new_achievements = self.service.check_new_achievements(user_id)

            # Assert
            self.assertEqual(len(new_achievements), 0)
            self.mock_repo.add_user_achievement.assert_not_called()

    def test_get_user_achievements(self):
        # Arrange
        user_id = 1
        earned_at = datetime.now()
        user_ach = UserAchievementORM(user_id=user_id, achievement_id=1, earned_at=earned_at)
        ach = AchievementORM(id=1, name="Test", description="Desc", icon_url="url")
        
        self.mock_repo.get_user_achievements_with_details.return_value = [(user_ach, ach)]

        # Act
        result = self.service.get_user_achievements(user_id)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")
        self.assertEqual(result[0].earned_at, earned_at)

    def test_check_new_achievements_commits(self):
        # Arrange
        user_id = 1
        # Mock achievement that is NOT earned yet
        ach = AchievementORM(id=1, name="Test", condition_type="REVIEW_COUNT", condition_params={"count": 5})
        self.mock_repo.get_all_achievements.return_value = [ach]
        self.mock_repo.get_user_achievement_ids.return_value = [] # User has none
        
        # Mock handler to return True (earned)
        mock_handler = MagicMock()
        mock_handler.check.return_value = True
        
        with patch.object(HandlerRegistry, 'get_handler', return_value=mock_handler):
            # Act
            self.service.check_new_achievements(user_id)

        # Assert
        # We expect commit to be called to save the new achievement
        # This will FAIL because of the early return in the service
        self.mock_db.commit.assert_called_once()

    def test_get_achievements_status(self):
        # Arrange
        user_id = 1
        ach1 = AchievementORM(id=1, name="Ach1", description="D1", condition_type="T1", condition_params={})
        ach2 = AchievementORM(id=2, name="Ach2", description="D2", condition_type="T2", condition_params={})
        self.mock_repo.get_all_achievements.return_value = [ach1, ach2]
        
        user_ach = UserAchievementORM(user_id=user_id, achievement_id=1, earned_at=datetime.now())
        self.mock_repo.get_user_achievements.return_value = [user_ach]

        # Act
        result = self.service.get_achievements_status(user_id)

        # Assert
        self.assertEqual(len(result), 2)
        # Ach1 should be earned
        self.assertEqual(result[0].id, 1)
        self.assertTrue(result[0].earned)
        # Ach2 should NOT be earned
        self.assertEqual(result[1].id, 2)
        self.assertFalse(result[1].earned)

if __name__ == '__main__':
    unittest.main()
