import unittest
from unittest.mock import MagicMock
from service.CacheService import CacheService

class TestCache(unittest.TestCase):

    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_config.get.return_value = 60
        self.service = CacheService(self.mock_config)
        self.service._cache = {} 

    def test_set_and_get(self):
        # Arrange
        key = "test_key"
        value = "test_value"

        # Act
        self.service.set(key, value)
        result = self.service.get(key)

        # Assert
        self.assertEqual(result, value)

    def test_get_missing(self):
        # Arrange
        key = "missing_key"

        # Act
        result = self.service.get(key)

        # Assert
        self.assertIsNone(result)

    def test_clear_all_starting_with(self):
        # Arrange
        self.service.set("prefix_1", "val1")
        self.service.set("prefix_2", "val2")
        self.service.set("other_1", "val3")

        # Act
        self.service.clear_all_starting_with("prefix_")

        # Assert
        self.assertIsNone(self.service.get("prefix_1"))
        self.assertIsNone(self.service.get("prefix_2"))
        self.assertEqual(self.service.get("other_1"), "val3")

if __name__ == '__main__':
    unittest.main()
