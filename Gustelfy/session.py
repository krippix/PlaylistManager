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
    db_con: database.Database
    user_id: str

    def __init__(self, spotify: spotify_api.Spotify_api, database: database.Database):
        self.logger = logging.getLogger("Gustelfy.session") #TODO include userid here once it's properly instancialized
        self.spotify = spotify
        self.db_con = database
        self.user_id = self.spotify.get_user_id()

    ##########
    # get

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
        result = {
            "display_name": self.spotify.get_display_name(),
            "playlists": self.spotify.fetch_playlists(),
            "changes": self.get_library_changes()
        }
        
        return result


    def get_library_changes(self) -> tuple[list[objects.track.Track],list[objects.track.Track]]:
        '''Returns tuple of list of changed tracks in library: (added,removed)'''

        local_lib = self.db_con.get_library(self.user_id)
        online_lib = self.spotify.fetch_library()

        # Creates list of songs that exist in both local and online library
        overlap = [local_track for local_track in local_lib for online_track in online_lib if local_track.get_id() == online_track.get_id()]

        added = []
        removed = []

        # Creates lists off added and removed songs
        for overlap_track in overlap:
            
            match_found = False
            for local_track in local_lib:
                if local_track.get_id() == overlap_track.get_id():
                    match_found = True
                    break
            if not match_found:
                removed.append(local_track)

            match_found = False
            for online_track in online_lib:
                if online_track.get_id() == overlap_track.get_id():
                    match_found = True
                    break
            if not match_found:
                added.append(online_track)

        return (added,removed)


    ##########
    # add / set

    def add_track(self, track: objects.track.Track):
        '''Attempts to add track to local database. Updates if already present and expired.'''
        
        # Check if track is already part of the database
        db_track = self.db_con.get_track(track.get_id())
        if db_track is None or track != db_track or db_track.is_expired():
            self.db_con.add_track(self.spotify.fetch_track(track))
        
        # check if artist information of track is up to date
        for artist in track.get_artists():
            db_artist = self.db_con.get_artist(artist.get_id())
            if db_artist is None or db_artist.is_expired():
                self.db_con.add_artist(self.spotify.fetch_artist())
            

    def update_library(self):
        '''Updates the current user's library in the database.'''
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
        '''Updates all track entries in database. This shouldnt change which songs are in the database but update names and artist information.'''

    
    def update_database_artists(self):
        '''Searches database for outdated artists.'''
        self.db_con.get_artist()


    def update_library(self):
        '''Updates users library'''

    ##########
    # compare


    ##########
    # webserver interfaces (?)


def kekw(a,b):
    print(f"a: {a}  b: {b}")
    if a==b:
        return a


def test():
    numbers = [1,2,3,4,5,6,'f']
    letters = ['a','b','c','d','e','f']

    test = [kekw(number,letter) for number in numbers for letter in letters]
    test = [i for i in test if i is not None]
    print(test)


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    test()
    exit()