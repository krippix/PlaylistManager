import secrets
from contextlib import asynccontextmanager

from backend.util import config

import spotipy
from fastapi import APIRouter
from fastapi import FastAPI
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
    )
    return RedirectResponse(auth_handler.get_authorize_url())


@router.get("/auth/callback")
async def callback(code: str, state: str):
    """
    This function is called by the spotify redirect, this is where the key will be provided and parsed.
    """
    auth_handler = spotipy.oauth2.SpotifyOAuth(scope=config.get_scopes(), open_browser=False)
    auth_handler.get_access_token(code=code)
    return {"code": code, "state": state}
