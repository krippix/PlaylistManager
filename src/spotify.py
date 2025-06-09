import spotipy

from .models import SpotifyCredentials


class UserCache(spotipy.CacheHandler):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_cached_token(self):
        #SpotifyCredentials.
        pass

    def save_token_to_cache(self, token_info):
        pass
