import time
import logging
from typing import Any, Optional
from service.ConfigService import ConfigService


class CacheService:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self._cache = {}
        self._ttl = self.config_service.get("cache_ttl_seconds", 60)
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"CacheService initialized. ID: {id(self)}")

    def get(self, key: str) -> Optional[Any]:
        self.logger.debug(f"Cache GET key='{key}'. Cache keys: {list(self._cache.keys())}")
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                self.logger.debug("Cache HIT")
                return data
            else:
                self.logger.debug("Cache EXPIRED")
                del self._cache[key]
        else:
            self.logger.debug("Cache MISS")
        return None

    def set(self, key: str, value: Any):
        self.logger.debug(f"Cache SET key='{key}'")
        self._cache[key] = (value, time.time())

    def clear_all_starting_with(self, prefix: str):
        keys_to_delete = [k for k in self._cache.keys() if k.startswith(prefix)]
        for k in keys_to_delete:
            del self._cache[k]

    def clear(self):
        self._cache.clear()
