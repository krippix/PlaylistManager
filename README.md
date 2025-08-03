# PlaylistManager

## Installation

In order to use this in a django project, install it there via pip.
Then place in in settings.py

```python
INSTALLED_APPS = [
  'django_playlist_manager.apps.PlaylistManagerConfig',
  ...
]
```

Additionally add it to the urls.py

```python
urlpatterns = [
    path("playlists/", include("django_playlist_manager.urls")),
    ...
]
```

## Setup

API KEY can be found here:
<https://developer.spotify.com/dashboard/>

The following environment variables have to be set:

| variable                | description                                                             |
|-------------------------|-------------------------------------------------------------------------|
| `SPOTIPY_REDIRECT_URI`  | Must match the redirect URI added to your application in your Dashboard |
| `SPOTIPY_CLIENT_SECRET` | As seen in the Spotify developer portal                                 |
| `SPOTIPY_CLIENT_ID`     | As seen in the Spotify developer portal                                 |
