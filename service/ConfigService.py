import json
import os
from typing import Any

class ConfigService:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = "app_config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self._config = json.load(f)
        else:
            self._config = {
                "registration_enabled": True,
                "default_page_size": 10,
                "cache_ttl_seconds": 60,
                "logging_level": "INFO",
                "database_url": "postgresql+psycopg2://postgres:@localhost:5151/fastapi_db"
            }

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
