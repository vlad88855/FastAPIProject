import unittest
from unittest.mock import MagicMock, patch
import json
from service.ConfigService import ConfigService

class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"key": "value"}')
    def test_load_config_success(self, mock_file, mock_exists):
        # Arrange
        mock_exists.return_value = True
        ConfigService._instance = None
        
        # Act
        service = ConfigService()

        # Assert
        self.assertEqual(service.get("key"), "value")

    @patch("os.path.exists")
    def test_load_config_file_not_found(self, mock_exists):
        # Arrange
        mock_exists.return_value = False
        ConfigService._instance = None
        
        # Act
        service = ConfigService()

        # Assert
        self.assertEqual(service.get("registration_enabled"), True)

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"key": "value"}')
    def test_get_with_default(self, mock_file):
        # Arrange
        ConfigService._instance = None
        service = ConfigService()

        # Act
        result = service.get("missing_key", "default_val")

        # Assert
        self.assertEqual(result, "default_val")

if __name__ == '__main__':
    unittest.main()
