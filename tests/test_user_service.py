import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from service.UserService import UserService
from repository.UserRepository import UserRepository
from service.ConfigService import ConfigService
from model.DTOs.UserDTO import UserCreate, UserOut, UserUpdate
from model.UserORM import UserORM, UserRole
from datetime import datetime

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock(spec=UserRepository)
        self.mock_config = MagicMock(spec=ConfigService)
        self.service = UserService(self.mock_repo, self.mock_config)

    # --- CRUD ---

    def test_create_success(self):
        # Arrange
        dto = UserCreate(username="testuser", email="test@example.com", password="password123")
        user_orm = UserORM(id=1, username="testuser", email="test@example.com", role=UserRole.USER, created_at=datetime.utcnow())
        
        self.mock_config.get.return_value = True
        self.mock_repo.create_user.return_value = user_orm

        # Act
        result = self.service.create_user(dto)

        # Assert
        self.assertEqual(result.id, 1)
        self.assertEqual(result.username, "testuser")
        self.mock_repo.create_user.assert_called_once_with(dto)

    def test_get_success(self):
        # Arrange
        user_id = 1
        user_orm = UserORM(id=user_id, username="test", email="test@test.com", role=UserRole.USER, created_at=datetime.utcnow())
        self.mock_repo.get_user.return_value = user_orm

        # Act
        result = self.service.get_user(user_id)

        # Assert
        self.assertEqual(result.id, user_id)
        self.mock_repo.get_user.assert_called_once_with(user_id)

    def test_update_success(self):
        # Arrange
        user_id = 1
        update_dto = UserUpdate(username="newname")
        user_orm = UserORM(id=user_id, username="newname", email="test@test.com", role=UserRole.USER, created_at=datetime.utcnow())
        self.mock_repo.update_user.return_value = user_orm

        # Act
        result = self.service.update_user(user_id, update_dto)

        # Assert
        self.assertEqual(result.username, "newname")
        self.mock_repo.update_user.assert_called_once_with(user_id, update_dto)

    def test_delete_success(self):
        # Arrange
        user_id = 1

        # Act
        self.service.delete_user(user_id)

        # Assert
        self.mock_repo.delete_user.assert_called_once_with(user_id)

    def test_create_duplicate(self):
        # Arrange
        dto = UserCreate(username="test", email="test@test.com", password="password")
        self.mock_config.get.return_value = True
        self.mock_repo.create_user.side_effect = Exception("Duplicate entry")

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.service.create_user(dto)
        
        self.assertEqual(context.exception.status_code, 409)

    def test_get_not_found(self):
        # Arrange
        user_id = 999
        self.mock_repo.get_user.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.service.get_user(user_id)
        
        self.assertEqual(context.exception.status_code, 404)

    def test_update_not_found(self):
        # Arrange
        user_id = 999
        update_dto = UserUpdate(username="newname")
        self.mock_repo.update_user.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.service.update_user(user_id, update_dto)
            
        self.assertEqual(context.exception.status_code, 404)

    def test_delete_not_found(self):
        # Arrange
        user_id = 999
        self.mock_repo.get_user.return_value = None 
        
        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.service.delete_user(user_id)
            
        self.assertEqual(context.exception.status_code, 404)

    # --- Collections ---

    def test_get_list_success(self):
        # Arrange
        user_orm = UserORM(id=1, username="test", email="t@t.com", role=UserRole.USER, created_at=datetime.utcnow())
        self.mock_repo.get_all_users.return_value = [user_orm]

        # Act
        result = self.service.get_all_users()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].username, "test")

    def test_get_list_empty(self):
        # Arrange
        self.mock_repo.get_all_users.return_value = []

        # Act
        result = self.service.get_all_users()

        # Assert
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    # --- Logic ---

    def test_create_user_registration_disabled(self):
        # Arrange
        dto = UserCreate(username="testuser", email="test@example.com", password="password123")
        self.mock_config.get.return_value = False

        # Act & Assert
        with self.assertRaises(HTTPException) as cm:
            self.service.create_user(dto)
        
        self.assertEqual(cm.exception.status_code, 403)
        self.mock_repo.create_user.assert_not_called()

    def test_update_partial_fields(self):
        # Arrange
        user_id = 1
        update_dto = UserUpdate(avatar_url="http://new.avatar")
        
        user_orm = UserORM(id=user_id, username="old", email="old@t.com", role=UserRole.USER, created_at=datetime.utcnow(), avatar_url="http://new.avatar")
        self.mock_repo.update_user.return_value = user_orm

        # Act
        result = self.service.update_user(user_id, update_dto)

        # Assert
        self.assertEqual(result.avatar_url, "http://new.avatar")
        self.mock_repo.update_user.assert_called_once_with(user_id, update_dto)

if __name__ == '__main__':
    unittest.main()
