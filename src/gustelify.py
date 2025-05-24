# external
import spotipy
# python native
import logging, time
# project
import spotify_api
import util.database
import objects.track

class Gustelify:
    '''Instance containing all actions a user can take(?)'''
    spotify: spotify_api.Spotify_api
    database: util.database.Database
    user_id: str

    def __init__(self, spotify: spotify_api.Spotify_api, database: util.database.Database):
        self.spotify = spotify
        self.database = database

    ##########
    # add / set

    def add_track(self, track: objects.track.Track):
        '''Adds track to local db.'''
    
    
    ##########
    # update

    def update_user(self):
        '''Updates the spotify users profile, including: library, playlists their content, genres and artist information.'''
        # check if displayname changed or smth like that

        # pull library

        # pull playlists


    def update_database(self):
        '''Updates database with songs in user's library and RELEVANT playlists.'''

    
    def update_track(self, track: objects.track.Track):
        '''Updates db entry of given track and updates provided object.'''

        timestamp = int(time.time())

        # Get existing track from database
        db_result = self.database.get_track(track.get_id())

        # if track doesent exist yet, create it properly
        if len(db_result) == 0:
            self.add_track(track)
            return

        if timestamp - track.get_timestamp() > 3600:
            api_result = self.spotify.get_track(track.get_id())
            #if db_result == 



    ##########
    # compare

    def compare_library(self) -> list[tuple[objects.track.Track,objects.track.Track]]:
        '''Compares user library to locally stored library image. Returns list of tuples containing (added,removed) tracks'''

        self.database.get_





if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()