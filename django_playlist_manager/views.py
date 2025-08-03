import functools

import spotipy
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render

import django_playlist_manager.spotify as djotify


def spotify_auth(func):
    """
    Attempts to connect to spotify, redirects to login on failure
    """
    @functools.wraps(func)
    def wrapped_func(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        spotify_auth = djotify.get_auth_obj(request.user.id)

        if not spotify_auth.cache_handler.get_cached_token():
            return HttpResponseRedirect('../') # TODO: make sure this redirects to a view instead of a path

        sp = spotipy.Spotify(auth_manager=spotify_auth)

        return func(request, *args, **kwargs, sp=sp)
    return wrapped_func


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    spotify_auth = djotify.get_auth_obj(request.user.id)

    if not spotify_auth.cache_handler.get_cached_token():
        return render(request, "index.html", {"spotify_auth_url": spotify_auth.get_authorize_url()})

    sp = spotipy.Spotify(auth_manager=spotify_auth)
    user_info = sp.current_user()

    page_data = {
        "display_name": user_info['display_name'],
        "user_url": user_info['external_urls']["spotify"],
        "followers": user_info['followers']['total'],
    }
    return render(request, "index.html", page_data)


@spotify_auth
def playlists(request: HttpRequest, *args, **kwargs):
    sp: spotipy.Spotify = kwargs['sp']
    fetched_playlists = djotify.fetch_all_user_playlists(sp)

    playlists: list[dict] = []

    # get all liked songs
    songs = set(djotify.fetch_all_saved_tracks(sp))

    for playlist in fetched_playlists:
        playlists.append({
            "name": playlist['name'],
            "id": playlist['id'],
            "image_url": playlist['images'][0]['url'] if playlist.get('images') else "",
            "url": playlist['external_urls']['spotify'],
            "tracks": djotify.fetch_all_playlist_tracks(sp, playlist['id']),
        })

    # add liked status to each track in each playlist
    for playlist in playlists:
        for track in playlist['tracks']:
            track['liked'] = track['id'] in songs

    page_data = {
        "playlists": playlists,
    }

    return render(request, "playlists.html", page_data)


def login(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()


def auth_callback(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    spotify_auth = djotify.get_auth_obj(request.user.id)
    code = spotify_auth.parse_response_code(request.get_full_path())
    token = spotify_auth.get_access_token(code=code)
    spotify_auth.cache_handler.save_token_to_cache(token_info=token)
    sp = spotipy.Spotify(auth=spotify_auth)

    return HttpResponse(f"{sp.current_user()}")
