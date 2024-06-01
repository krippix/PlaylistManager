"""
Provides custom Cache Handler to allow for multiple users.
"""
from spotipy import CacheHandler

from backend.util.database import Database
from backend.util import config


class DictCacheHandler(CacheHandler):
    """
    Saves last provided token dict. Does not really keep track of cached tokens.
    """
    def __init__(self):
        self.token = {}

    def get_cached_token(self):
        return None

    def save_token_to_cache(self, token_info):
        self.token = token_info

    def get_dict(self) -> dict:
        return self.token


class SqliteCacheHandler(CacheHandler):
    """
    Caches tokens in sqlite database.
    """
    def __init__(self, database_connection: Database, user_id: str):
        self.database_connection = database_connection
        self.user_id = user_id

    def get_cached_token(self):
        """
        Get and return a token_info dictionary object.
        """
        return config.database.get_token(self.user_id)

    def save_token_to_cache(self, token_info):
        """
        Save a token_info dictionary object to the cache and return None.
        """
        config.database.set_token(self.user_id, token_info)
