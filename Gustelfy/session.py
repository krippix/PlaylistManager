# external
# python native
import logging, time
# project
import spotify_api, database
import util.config
import objects.track

class Session:
    '''Entrypoint for any data manipulation. Combines database and spotify API access. This will (probably) represent a user session.'''
    spotify: spotify_api.Spotify_api
    database: database.Database
    user_id: str

    def __init__(self, spotify: spotify_api.Spotify_api, database: database.Database):
        self.spotify = spotify
        self.database = database

    ##########
    # add / set

    def add_track(self, track: objects.track.Track):
        '''Adds track to local db.'''
        db_track = self.database.get_track(track.get_id())
        if db_track is None or track != db_track or db_track.is_expired():
            self.database.add_track(self.spotify.fetch_track(track))
        
        # check if artist information of track is up to date
        for artist in track.get_artists():
            db_artist = self.database.get_artist(artist.get_id())
            if db_artist is None or db_artist.is_expired():
                self.database.add_artist(self.spotify.fetch_artist())
            

    def add_library(self):
        '''Adds users library to the database'''
        library = self.spotify.fetch_library()

        for track in library:
            self.add_track(track)


    ##########
    # update

    def update_user(self):
        '''Updates the spotify users profile, including: library, playlists their content, genres and artist information.'''
        # check if displayname changed or smth like that

        # pull library

        # pull playlists


    def update_database(self):
        '''Updates database with songs in user's library and RELEVANT playlists.'''

    
    def update_database_artists(self):
        '''Searches database for outdated artists.'''
        self.database.get_artist()

    
    def update_tracks(self):
        '''Updates all track entries in database.'''

    def update_library(self):
        '''Updates users library'''

    ##########
    # compare

    def compare_library(self) -> list[tuple[objects.track.Track,objects.track.Track]]:
        '''Compares user library to locally stored library image. Returns list of tuples containing (added,removed) tracks'''

        #self.database.get_





if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()