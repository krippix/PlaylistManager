# GustelifyPlaylistMgr

## Setup

API KEY can be found here:
<https://developer.spotify.com/dashboard/>


`python -m Gustelfy`

## Ziel / Goal

Ziel dieser Software ist es, es mehreren Benutzern zu ermöglichen ihre Playlists nach dem von mir genutzten System zu sortieren:
- Zentral für die Verwaltung ist ob ein song einen "like" hat
- Bestimmte Playlists agieren als sogenannte "Genre-Playlists", ein song mit einem like muss in einer dieser Playlists vorkommen
- Gibt ein Benutzer einem Song einen Like, soll er (z.B. an einem Stichtag) entscheiden in welche der Genre-Playlists der Song kommen soll
- Entfernt ein Benutzer den Like eines songs, soll er aus allen genre-playlists entfernt werden (Keine Interaktion notwendig)
- Entfernte songs sollen in einer Art "Friedhof" landen, damit in Zukunft noch auf sie zugegriffen werden kann

Die Datenbank soll dabei dafür sorgen dass die API Anfragen auf ein Mindestmaß begrenzt werden. 
Gleichzeitig wird über die Datenbank festgestellt welche Änderungen stattgefunden haben.
Zusätzlich werden die Benutzerdaten dort gespeichert.

---

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

## ToDo

- [ ] figure out how to work user independent
- [ ] implement pairing table usage
