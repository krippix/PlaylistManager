# external
# python native
import logging
import time
# project
from Gustelfy import spotify_api
from Gustelfy.database import database
from Gustelfy.util import config
from Gustelfy.objects import track, playlist


class Session:
    '''Entrypoint for any data manipulation. Combines database and spotify API access. This will (probably) represent a user session.'''
    
    spotify: spotify_api.Spotify_api
    db_con: database.Database
    user_id: str

    def __init__(self, spotify: spotify_api.Spotify_api, database: database.Database):
        self.spotify = spotify
        self.db_con = database
        self.user_id = self.spotify.get_user_id()
        self.logger = logging.getLogger(f"Gustelfy.session.{self.user_id}")
        self.logger.info("Initialized session.")

    # ---- Getter Functions ----

    def get_homepage_data(self) -> dict:
        '''
        Returns data needed for homepage. 
        {
            display_name: <username>,
            playlists: [(name,isGenrePlaylist),...],
            changes: ([added],[removed])
        }
        # TODO somehow have to recieve the users decisions from the flask server.
        '''
        self.logger.debug("get_homepage_data()")

        result = {
            "display_name": self.spotify.get_display_name(),
            "playlists": self.spotify.fetch_playlists(),
            "changes": self.get_library_changes()
        }
        return result

    def get_library_changes(self) -> tuple[list[track.Track],list[track.Track]]:
        '''Returns tuple of list of changed tracks in library: (added,removed)'''
        self.logger.debug("get_library_changes()")

        local_lib = self.db_con.get_library(self.user_id)
        online_lib = self.spotify.fetch_library()

        # Creates list of songs that exist in both local and online library
        overlap = [local_track for local_track in local_lib for online_track in online_lib if local_track.get_id() == online_track.get_id()]

        added = []
        removed = []

        # Create list of removed tracks
        for local_track in local_lib:
            match_found = False
            for overlap_track in overlap:
                if local_track.get_id() == overlap_track.get_id():
                    match_found = True
                    break
            if not match_found:
                removed.append(local_track)
        
        # Create list of added tracks
        for online_track in online_lib:
            match_found = False
            for overlap_track in overlap:
                if online_track.get_id() == overlap_track.get_id():
                    match_found = True
                    break
            if not match_found:
                added.append(online_track)
        
        self.logger.info(f"{len(added)} new tracks added.")
        self.logger.info(f"{len(removed)} tracks have been removed.")

        return (added,removed)

    def get_playlists(self) -> list[playlist.Playlist]:
        '''Kicks of updates of the users local playlists, returns current state of them.'''
        self.logger.debug(f"get_playlists()")

        self.update_playlists()

    # ---- Setter Functions ----

    # ---- Other Functions ----

    # -- add --

    def add_track(self, track: track.Track):
        '''Attempts to add track to local database. Updates if already present and expired.'''
        self.logger.debug("add_track()")
        
        # Check if track is already part of the database
        db_track = self.db_con.get_track(track.get_id())
        if db_track is None or track != db_track or db_track.is_expired():
            self.db_con.add_track(self.spotify.fetch_track(track))
        
        # check if artist information of track is up to date
        for artist in track.get_artists():
            db_artist = self.db_con.get_artist(artist.get_id())
            if db_artist is None or db_artist.is_expired():
                self.db_con.add_artist(self.spotify.fetch_artist())
            
    def commit_library_changes(self, changes: tuple[list[track.Track],list[track.Track]]):
        '''Updates the current user's library in the database.'''
        self.logger.debug("update_library()")

        library = self.spotify.fetch_library()

        for track in library:
            self.add_track(track)
        self.db_con.update_library(self.user_id, changes)

    # -- update --

    def update_user(self):
        '''Updates the spotify users profile, including: library, playlists their content, genres and artist information.'''
        self.logger.debug("update_user()")
        
        # check if displayname changed or smth like that

        # pull library

        # pull playlists

    def update_database(self):
        '''Updates all track entries in database. This shouldnt change which songs are in the database but update names and artist information.'''
        self.logger.debug("update_database()")
    
    def update_database_artists(self):
        '''Searches database for outdated artists.'''
        self.logger.debug("update_database_artists()")

        self.db_con.get_artist()

    def update_library(self):
        '''Updates users library'''
        self.logger.debug("update_library()")

    def update_playlists(self):
        '''Pulls current playlist state from spotify api, updates local db entry.'''
        self.logger.debug(f"update_playlists()")

        online_playlists = self.spotify.fetch_playlists()
        db_playlists = self.db_con.get_playlists(self.user_id)



    ##########
    # compare


    ##########
    # webserver interfaces (?)


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()