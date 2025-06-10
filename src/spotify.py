import spotipy
from django.db import models

from .models import SpotifyCredentials


class UserCache(spotipy.CacheHandler):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_cached_token(self):
        try:
            token = SpotifyCredentials.objects.get(django_user=self.user_id)
        except models.Model.DoesNotExist:
            return None
        return token

    def save_token_to_cache(self, token_info):
        pass
