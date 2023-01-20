# external
import sqlite3
# python native
import logging
import os
import time
from pathlib import Path
from abc import ABC, abstractmethod
# project
from Gustelfy.database import interface
from Gustelfy.util import config, helper
from Gustelfy.objects import *


class SqliteCon(interface.Interface):
    """Implements DatabaseConnection for sqlite3 interface"""

    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    # ---- Getter Functions ----

    def get_album(self, id: str) -> album.Album | None:
        """Returns album with given id."""
        # TODO

    def get_artist(self, id: str) -> artist.Artist | None:
        """Returns artist object or None if nothing was found."""
        db_result = self.cursor.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (id,)).fetchall()
        
        if len(db_result) == 1:
            return artist.Artist(id=db_result[0][0], name=db_result[0][1], timestamp=db_result[0][2])
        else:
            return None

    def get_favorites(self, user_id: str) -> list[track.Track]:
        """Returns list of songs withing the user"""
        result_list = []
        db_result = self.cursor.execute("SELECT tracks_id_fkey FROM libraries WHERE users_id_fkey=?",(user_id,)).fetchall()

        if db_result:
            for track in db_result:
                result_list.append(self.get_track(track[0]))
        return result_list

    def get_genres(self, artist_id: str) -> list[str]:
        """Returns list of genres associated with the given artist"""
        result_list = []
        db_result = self.cursor.execute("SELECT genres.name FROM genres JOIN genres ON genres.id_pkey=artists_genres.genres_id_fkey WHERE artists.id_pkey=?", (artist.get_id(),)).fetchall()
        for item in db_result:
            result_list.append(item)
        return result_list

    def get_playlist(self, id: str) -> playlist.Playlist | None:
        """Returns playlist object or None if nothing was found."""
        db_result = self.cursor.execute("SELECT id_pkey,name,isgenreplaylist FROM playlists WHERE users_id_fkey=?",(user_id,)).fetchall()

        playlists = []
        for _playlist in db_result:
            playlists.append(playlist.Playlist(id=_playlist[0],name=_playlist[1],owner_id=user_id,is_managed=bool(_playlist[2])))
            # Include tracks within playlist
            db_result = self.cursor.execute("SELECT tracks.id_pkey FROM tracks INNER JOIN playlists_content ON tracks.id_pkey=playlists_content.tracks_id_fkey WHERE playlists_content.playlists_id_fkey=?",(_playlist[0],)).fetchall()
            tracks = []
            for track in db_result:
                tracks.append(self.get_track(track[0]))
        return playlists

    def get_track(self, id: str) -> track.Track | None:
        """Returns track object. Or None, if nothing was found."""
        db_result = self.cursor.execute("SELECT id_pkey,name,timestamp FROM tracks WHERE id_pkey=?",(id,)).fetchall()
        self.logger.debug(f"SELECT FROM: {db_result}")

        if len(db_result) == 0:
            return None
        else:
            return track.Track(
                id=db_result[0][0],
                name=db_result[0][1],
                timestamp=db_result[0][2],
                artists=self._get_track_artists(id)
            )

    def get_user(self, id: str) -> user.User | None:
        """Returns user object with given id."""
        # TODO

    def _get_track_artists(self, track_id: str) -> artist.Artist | None:
        """Returns all artists accociated with the given track id."""
        result_list = []
        db_result = self.cursor.execute("SELECT artists_id_fkey from tracks_artists WHERE tracks_id_fkey=?",(track_id,)).fetchall()

        for item in db_result:
            next_result = self.get_artist(item[0])
            next_result.set_genres(next_result)
            result_list.append(next_result)
        return result_list

    # ---- Setter Functions ----

    # ---- Other Functions ----

    def connect_database(self):
        """Establishes connection to database"""
        self.logger = logging.getLogger(__name__)
        self.connection = sqlite3.connect(self.settings.get_dbpath())
        self.cursor = self.connection.cursor()
        self.check()

    # -- add --
    
    def add_album(self, album: album.Album):
        """Adds an album to the database. Overwrites if already present."""

    def add_artist(self, artist: artist.Artist):
        """Adds an artist to the database. Overwrites if already present."""
        timestamp = int(time.time())

        db_result = self.cursor.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (artist.get_id(),)).fetchall()

        if len(db_result) == 0:
            self.cursor.execute("INSERT INTO artists (id_pkey,name,timestamp) VALUES (?,?,?)",(artist.get_id(), artist.get_name(), timestamp))
        else:
            self.cursor.execute("UPDATE artists SET name = ?, timestamp = ? WHERE id_pkey = ?",(artist.get_name(), timestamp, artist.get_id()))
        
        # TODO handle genres for provided artist

        self.connection.commit()

    def add_favorite(self, user: user.User, track: track.Track):
        """Adds a favorite to the database. Overwrites if already present."""

    def add_genre(self, genre: str):
        """Adds a genre to the database. Overwrites if already present."""

    def add_playlist(self, playlist: playlist.Playlist):
        """Adds a playlist to the database. Overwrites if already present."""    

    def add_track(self, track: track.Track):
        """Adds a track to the database. Overwrites if already present."""
        # attempt to pull track with given track id from database
        db_result = self.cursor.execute("SELECT id_pkey,name,timestamp FROM tracks WHERE id_pkey == ?", (track.get_id(),)).fetchall()

        # if nothing is found, simply add the new song into the db, else update entry
        if len(db_result) == 0:
            self.cursor.execute("INSERT INTO tracks (id_pkey,name,timestamp) VALUES (?,?,?)", (track.get_id(), track.get_name(), int(time.time())))
        else:
            self.cursor.execute("UPDATE tracks SET name = ?, timestamp = ? WHERE id_pkey = ?", (track.get_name(), track.get_timestamp(), track.get_id()))

        # now ensure all involved artists also exist within the database
        rebuild_track_artists = False
        db_result = self.cursor.execute("SELECT artists_id_fkey FROM tracks_artists WHERE tracks_id_fkey=?",(track.get_id(),)).fetchall()
        
        for artist in track.get_artists():
            self.add_artist(artist)

            # Check if song has same amount of artists
            if len(db_result) == len(track.get_artists()):
                if artist.get_id() not in db_result:
                    rebuild_track_artists = True
            else:
                rebuild_track_artists = True

        if rebuild_track_artists:
            self.cursor.execute("DELETE FROM tracks_artists WHERE tracks_id_fkey=?",(track.get_id(),))
            for artist in track.get_artists():
                self.cursor.execute("INSERT INTO tracks_artists (tracks_id_fkey,artists_id_fkey) VALUES (?,?)",(track.get_id(),artist.get_id()))
        self.connection.commit()

    def add_user(self, user: user.User):
        """Adds a user to the database. Overwrites if already present."""

    # -- Update --

    def update_favorites(self, user_id, delta: tuple[list[track.Track], list[track.Track]]):
        """Updates list of favorites with given input

        Args:
            delta (tuple[list[track.Track], list[track.Track]]): 0 - added tracks; 1 - removed tracks
        """
        for track in delta[0]:
            self.cursor.execute("INSERT INTO libraries (users_id_fkey,tracks_id_fkey) VALUES (?,?)",(user_id,track.get_id()))

        for track in delta[1]:
            self.cursor.execute("DELETE FROM libraries WHERE tracks_id_fkey=?",(track.get_id(),))
        self.connection.commit()

    # -- Database integrity --

    def check(self):
        """Checks if the database contains all required tables. Attempts to fix any problems."""
        default_structure = helper.json_to_dict(os.path.join(self.settings.get_datafolder(),"sqlite3_conf.json"))

        for table in default_structure:
            if not self.table_exists(table):
                self.logger.error(f"Table {table} is missing. Creating replacement...")
                self.cursor.execute(default_structure[table])
        self.connection.commit()

    def create_database(self):
        """Creates Database structure."""

    def table_exists(self, table: str) -> bool:
        """Checks if provided table exists."""
        result = self.cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name = ?;", (table,)).fetchall()

        if len(result) == 0:
            return False
        if len(result) == 1:
            return True
        self.logger.critical("Table appears to exist multiple times. Database may be inconsistent.")


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()