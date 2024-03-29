# external
# python native
import logging
import time
# project
from Gustelfy import spotify_api
from Gustelfy import database
from Gustelfy.database import interface
from Gustelfy.util import config
from Gustelfy.objects import album, artist, playlist, track, user


class Session:
    '''Entrypoint for any data manipulation. Combines database and spotify API access. This will (probably) represent a user session.'''
    
    spotify: spotify_api.Spotify_api
    db_con: interface.Interface
    user: user.User

    def __init__(self, user: user.User, spotify: spotify_api.Spotify_api, database: interface.Interface):
        self.spotify = spotify
        self.db_con = database
        self.user = user
        self.logger = logging.getLogger(f"{__name__}:{user.get_id()}")
        self.logger.info("Initialized session.")

        self.db_con.add_user(self.user)

    # ---- TEMPORARY ASSIGNMENT FUNCTIONS ----
    # Used for my class project, will be removed together with the oracle db connection
    def dbp_fill_db(self):
        # The following have to be satisfied:
        self.db_con.add_user(self.spotify.fetch_current_user())
        # - favorites -> starting point
        for favorite in self.spotify.fetch_favorites():
            self.db_con.add_favorite(self.spotify.get_user_id(),favorite)
        # - album -> from all tracks that exist
        # - artist -> also from existing tracks and albums
        # - playlist -> from user
        playlists = self.spotify.fetch_playlists()
        full_playlists = []
        for pl in playlists:
            full_playlists.append(self.spotify.fetch_playlist(pl.get_id()))
        for full_playlist in full_playlists:
            self.db_con.add_playlist(full_playlist)
        # - track -> pulled from the other objects
        
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
            "changes": self.get_favorites_changes()
        }
        return result

    def get_favorites_changes(self) -> tuple[list[track.Track],list[track.Track]]:
        '''Returns tuple of list of changed tracks in favorites: (added,removed)'''
        self.logger.debug("get_favorites_changes()")

        local_lib = self.db_con.get_favorites(self.user.get_id())
        online_lib = self.spotify.fetch_favorites()

        # Creates list of songs that exist in both local and online favorites
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
        '''Kicks off updates of the users local playlists, returns current state of them.'''
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
            self.db_con.add_track(self.spotify.fetch_track(track.get_id()))
        
        # check if artist information of track is up to date
        for artist in track.get_artists():
            db_artist = self.db_con.get_artist(artist.get_id())
            if db_artist is None or db_artist.is_expired():
                self.db_con.add_artist(self.spotify.fetch_artist())
            
    def commit_favorites_changes(self, changes: tuple[list[track.Track],list[track.Track]]):
        '''Updates the current user's favorites in the database.'''
        self.logger.debug("update_favorites()")

        favorites = self.spotify.fetch_favorites()

        for track in favorites:
            self.add_track(track)
        self.db_con.update_favorites(self.user.get_id(), changes)

    # -- update --

    def update_user(self):
        '''Updates the spotify users profile, including: favorites, playlists their content, genres and artist information.'''
        self.logger.debug("update_user()")
        
        # check if displayname changed or smth like that

        # pull favorites

        # pull playlists

    def update_database(self):
        """This fills up all null values in the database and updates old database entries.
        """
        self.logger.debug("update_database()")
        result = self.db_con.get_incomplete_all()
        # albums
        for alb in result["albums"]:
            self.logger.info(f"Updating album {alb}")
            self.db_con.add_album(self.spotify.fetch_album(alb))
        """
        # artists
        for art in result["artists"]:
            self.logger.info(f"Updating artist {art}")
            self.db_con.add_artist(self.spotify.fetch_artist(art))
        # playlists
        for lst in result["playlists"]:
            self.logger.info(f"Updating playlist {lst}")
            self.db_con.add_playlist(self.spotify.fetch_playlist(lst))
        # tracks
        for trk in result["tracks"]:
            self.logger.info(f"Updating track {trk}")
            self.db_con.add_track(self.spotify.fetch_track(trk))
        self.logger.info("Updating database finished")
        """
        

    def update_database_artists(self):
        '''Searches database for outdated artists.'''
        self.logger.debug("update_database_artists()")

        self.db_con.get_artist()

    def update_favorites(self):
        '''Updates users favorites'''
        self.logger.debug("update_favorites()")

    def update_playlists(self):
        '''Pulls current playlist state from spotify api, updates local db entry.'''
        self.logger.debug(f"update_playlists()")

        online_playlists = self.spotify.fetch_playlists()
        db_playlists = self.db_con.get_playlists(self.user_id)
        

if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()