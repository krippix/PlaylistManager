# GustelfyPlaylists

## Configuration

The backend configuration is handled by environment variables.
Required keys are marked with a *

| variable                  | example value                      | description |
|:--------------------------|:-----------------------------------|-------------|
| `SPOTIPY_CLIENT_ID`*      | `cdef012345678abcdef012345678abcd` |             |
| `SPOTIPY_CLIENT_SECRET`*  | `678abcdef012345678abcdef01234567` |             |
| `SPOTIPY_REDIRECT_URI`*   | `https://example.com/spotify`      |             |

## Project Goal

This small software is supposed to manage Spotify Playlists, the Playlists to be managed have to be chosen explicitly.

The core idea(s) so far.

- each liked song belongs in a genre-playlist e.g. HipHop, Rock, Metal. These are user-defined.
- Upon liking, the genre is chosen automatically, but it can be changed (maybe drop-down?)
- Songs that lost their like are moved to a "graveyard" playlist
- Songs that gain a like are added to genre playlist
- maybe other like-only playlists

## Implementation

### Frontend

JavaScript Node Application accessing the backend via its API.

### Backend

Python REST API written with FastAPI

Start by typing: `python -m uvicorn backend.main:app --reload`

Documentation at: <http://localhost:8000/docs>
