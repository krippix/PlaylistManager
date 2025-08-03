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


def fetch_all_saved_tracks(sp: spotipy.Spotify) -> list[str]:
    limit = 50
    current_page: dict | None = sp.current_user_saved_tracks(limit=limit, offset=0)

    if not current_page:
        return []

    total = current_page.get("total", 0)

    result = [x["track"]["id"] for x in current_page["items"]]

    for i, _ in enumerate(range(total // limit)):
        offset = i * limit + limit
        current_page = sp.current_user_saved_tracks(limit=limit, offset=offset)

        if current_page is None:
            continue

        result += [x["track"]["id"] for x in current_page["items"]]

    return result


def fetch_all_user_playlists(sp: spotipy.Spotify) -> list[dict]:
    limit = 50
    current_page: dict | None = sp.current_user_playlists(limit=limit, offset=0)

    user = sp.current_user()
    if user is None:
        raise Exception("Spotify user has no id.")

    user_id = user["id"]

    if not current_page:
        return []

    total = current_page.get("total", 0)

    playlists = [x for x in current_page["items"] if x["owner"]["id"] == user_id]

    for i, _ in enumerate(range(total // limit)):
        offset = i * limit + limit
        current_page = sp.current_user_playlists(limit=limit, offset=offset)

        if current_page is None:
            continue

        playlists += [x for x in current_page["items"] if x["owner"]["id"] == user_id]

    return playlists


def fetch_all_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> list[dict]:
    """_summary_

    :param sp: _description_
    :param playlist_id: _description_
    :return: _description_

    ## Example item:
    ```
    {
        "album": {},
        "artists": [],
        "available_markets": [],
        "disc_number": 0,
        "duration_ms": 0,
        "explicit": false,
        "external_ids": {
            "isrc": "string",
            "ean": "string",
            "upc": "string"
        },
        "external_urls": {
            "spotify": "string"
        },
        "href": "string",
        "id": "string",
        "is_playable": false,
        "linked_from": {},
        "restrictions": {
            "reason": "string"
        },
        "name": "string",
        "popularity": 0,
        "preview_url": "string",
        "track_number": 0,
        "type": "track",
        "uri": "string",
        "is_local": false
    }
    ```
    """
    limit = 100
    current_page: dict | None = sp.playlist_items(playlist_id=playlist_id, limit=limit, additional_types=["track"])

    if current_page is None:
        return []

    total = current_page["total"]

    tracks = [x['track'] for x in current_page["items"]]
    for i, _ in enumerate(range(total // limit)):
        offset = i * limit + limit
        current_page = sp.playlist_items(
            playlist_id=playlist_id, limit=limit, offset=offset, additional_types=["track"]
        )

        if current_page is None:
            continue

        tracks += [x['track'] for x in current_page["items"]]

    return tracks
