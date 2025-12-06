# import unittest
# from unittest.mock import MagicMock
# from fastapi.testclient import TestClient
# from main import app
# from service.AchievementService import AchievementService
# from model.DTOs.AchievementDTO import AchievementOut, UserAchievementOut
# from datetime import datetime
#
# class TestAchievementViews(unittest.TestCase):
#
#     def setUp(self):
#         self.client = TestClient(app)
#         self.mock_service = MagicMock(spec=AchievementService)
#         app.dependency_overrides[AchievementService] = lambda: self.mock_service
#
#     def tearDown(self):
#         app.dependency_overrides = {}
#
#     def test_get_my_achievements(self):
#         pass
#
# if __name__ == '__main__':
#     unittest.main()
