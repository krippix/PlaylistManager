import os
import sys

import spotipy
from django.core.exceptions import ObjectDoesNotExist

import django_playlist_manager.models as models


class UserCache(spotipy.CacheHandler):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_cached_token(self):
        try:
            credentials = models.SpotifyCredentials.objects.get(django_user=self.user_id)
        except Exception as e:
            print(f"No credentials found for user with id {self.user_id}: {e}", file=sys.stderr)
            return None
        return credentials.token_info

    def save_token_to_cache(self, token_info):
        try:
            credentials = models.SpotifyCredentials.objects.get(django_user__id=self.user_id)
            credentials.token_info = token_info
        except ObjectDoesNotExist as e:
            print(f"No credentials found for user with id {self.user_id}: {e}", file=sys.stderr)
            credentials = models.SpotifyCredentials(django_user_id=self.user_id, token_info=token_info)
        credentials.save()


def get_auth_obj(user_id: int) -> spotipy.SpotifyOAuth:
    auth_obj = spotipy.SpotifyOAuth(
        scope="user-library-read",
        cache_handler=UserCache(user_id),
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        open_browser=False,
    )
    return auth_obj
