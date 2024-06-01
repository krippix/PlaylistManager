# GustelfyPlaylists

## Goal

This software is supposed to help with the organization of my playlists.
I want it to handle the following things:

- When a song is liked, add it to one of my (previously specified) genre-playlists
- When a song like is removed, remove it from each playlist that has been marked as "managed"
- When a song is removed, add it to a graveyard playlist
- Randomize order of songs in playlists
- Suggestions for classical music, but without duplicates

## Configuration

The backend configuration is handled by environment variables.
Required keys are marked with a *

| variable                  | example value                      | description |
|:--------------------------|:-----------------------------------|-------------|
| `SPOTIPY_CLIENT_ID`*      | `cdef012345678abcdef012345678abcd` |             |
| `SPOTIPY_CLIENT_SECRET`*  | `678abcdef012345678abcdef01234567` |             |
| `SPOTIPY_REDIRECT_URI`*   | `https://example.com/spotify`      |             |
