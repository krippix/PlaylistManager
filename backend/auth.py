from datetime import datetime
from datetime import timezone
import secrets
from http import HTTPStatus

from backend.util import config
from backend.util import cache_handler

import spotipy
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get("/login")
async def login() -> RedirectResponse:
    """
    Starts the login process by generating a login request for spotify.
    """
    callback_key = secrets.token_urlsafe(30)
    auth_handler = spotipy.oauth2.SpotifyOAuth(
        scope=config.get_scopes(),
        open_browser=False,
        state=callback_key,
        cache_handler=None
    )
    callback_key_expiry = int(datetime.now(timezone.utc).timestamp()) + 3600
    config.database.set_callback_key(callback_key, callback_key_expiry)
    return RedirectResponse(auth_handler.get_authorize_url())


@router.get("/callback")
async def callback(code: str, state: str):
    """
    This function is called by the spotify redirect, this is where the key will be provided and parsed.
    """
    if not config.database.valid_callback_key(state):
        raise HTTPException(status_code=400, detail="Invalid state")
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
