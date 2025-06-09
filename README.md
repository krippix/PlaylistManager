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

| variable               | description |
|------------------------|-------------|
| `SPOTIPY_REDIRECT_URI` | Must match the redirect URI added to your application in your Dashboard |
|   |   |
|   |   |

## Goal

This is an attempt at automatically sorting my Spotify music using the follwing scheme:

- Define Genre Playlists for all Songs I have liked (hearted)
- Once a heart is removed the follwing things happen:
  - song is removed from Genre playlist(s)
  - song will be put into a playlist with all other removed songs
- once a heart is added to a song the following things will happen:
  - queue song for adding to genre playlist (will probably be done manually)
  - remove song from deleted songs playlist
- adding new songs to genre playist will maybe be done via email? dunno yet

## Data within the database

The follwing data will be saved in the database

- albums
- artists
- favorites
- genres
- playlists
- tracks
- users

## Development

Local setup:

```shell
uv venv
source .venv/bin/activate
uv sync --dev
```

Build the package
```sh

```