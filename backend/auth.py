import secrets
from contextlib import asynccontextmanager

from backend.util import config
from backend.util import cache_handler

import spotipy
from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get("/auth/login")
async def login() -> RedirectResponse:
    """
    Starts the login process by generating a login request for spotify.
    """
    token = secrets.token_urlsafe(30)
    auth_handler = spotipy.oauth2.SpotifyOAuth(
        scope=config.get_scopes(),
        open_browser=False,
        state=token,
        cache_handler=None
    )
    return RedirectResponse(auth_handler.get_authorize_url())


@router.get("/auth/callback")
async def callback(code: str, state: str):
    """
    This function is called by the spotify redirect, this is where the key will be provided and parsed.
    """
    cache = cache_handler.DictCacheHandler()
    auth_handler = spotipy.oauth2.SpotifyOAuth(
        scope=config.get_scopes(),
        open_browser=False,
        cache_handler=cache
    )
    token = auth_handler.get_access_token(code=code)

    # Find out who the user sending the request is
    spotify_con = spotipy.Spotify(auth=token['access_token'])
    current_user = spotify_con.current_user()

    # write received user and token to the database
    config.database.set_user(
        current_user['id'],
        display_name=current_user['display_name'],
        access_token=token['access_token'],
        token_type=token['token_type'],
        expires_in=token['expires_in'],
        refresh_token=token['refresh_token'],
        scope=token['scope'],
        expires_at=token['expires_at']
    )
    return RedirectResponse('/?success=true')
