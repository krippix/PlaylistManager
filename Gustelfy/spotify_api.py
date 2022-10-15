# external
import spotipy
# python native
import logging, time
# project
import util.config
import objects.track, objects.artist, objects.playlist

# TODO this should be made back into instances (probably)
class Spotify_api:
    '''Class containing the spotify API connection, singleton.'''
    
    _instance = None
    spotify: spotipy.Spotify
    settings: util.config.Config
    client_id: str
    client_secret: str
    scopes = [
            "user-library-read",
            "user-library-modify",
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-read-collaborative",
            "playlist-modify-public"
        ]

    def __init__(self):
        # fetch credentials from config.ini
        self.settings = util.config.Config()
        self.client_id = self.settings.get_config("AUTH","client_id")
        self.client_secret = self.settings.get_config("AUTH","client_secret")

        # Authorize Application and user with Spotify
        
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=self.scopes,
            client_id=self.client_id,
            client_secret=self.client_secret,
            #open_browser=False,
            #show_dialog=True,
            redirect_uri="http://172.0.0.1:9090"
        )

        # connect to spotify
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)


    def __new__(cls):
        # this should make this class a singleton
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


    def check_credentials(self):
        '''Checks if any credentials have been provided in config.ini'''
        missing_credentials = False
        
        if len(self.client_id) == 0:
            logging.critical("No client id has been provided, please add one to data/config.ini")
            missing_credentials = True
        if len(self.client_secret) == 0:
            logging.critical("No client secret has been provided, please add one to data/config.ini")
            missing_credentials = True
        
        if missing_credentials:
            logging.info("Exiting software.")
            exit()

    def get_connection(self) -> spotipy.Spotify:
        return self.spotify

    ############
    # get
    ############

    def fetch_track(self, track: objects.track.Track):
        '''Pulls track from spotify api by id.'''
        result = self.spotify.track(track_id=track.get_id())

        if result is None:
            # TODO might need error handling here
            logging.error("Track not found in spotify db.")
            return None

        # add artists ids into list
        artists = []
        for artist in result["artists"]:
            artists.append(objects.artist.Artist(id=artist["id"], name=artist["name"], timestamp=int(time.time())))

        return objects.track.Track(id=track.get_id(), name=result["name"], artists=artists, timestamp=int(time.time()))


    def fetch_track_artists(self, track: objects.track.Track) -> objects.track.Track:
        '''Appends artist information to track object, and updates the involved artists'''
        artists = []

        for artist in track.get_artists():
            result = self.spotify.artist(artist.get_id())
            artists.append(objects.artist.Artist(id=artist.get_id(), name=result["name"], genres=result["genres"]))

        track.set_artists(artists)
        return track
    

    def fetch_artist(self, id: str) -> objects.artist.Artist:
        '''Returns one artist based on input id.'''
        


    def fetch_library(self) -> list[objects.track.Track]:
        '''Takes all tracks from users library and returns them as List of song objects'''
        result_list = []

        # fetch library
        done = False
        offset = 0

        # iterate over library
        while not done:
            results = self.spotify.current_user_saved_tracks(limit=50,offset=offset)

            if len(results["items"]) < 50:
                done = True
            
            for track in results["items"]:
                track = track["track"]
                
                # put artists into one list
                artists = []
                for artist in track["artists"]:
                    artists.append(objects.artist.Artist(artist["id"],artist["name"], timestamp=int(time.time())))
                
                result_list.append(objects.track.Track(id=track["id"],name=track["name"],artists=artists, timestamp=int(time.time())))
            offset += 50
        return result_list


    def fetch_playlists(self):
        '''Returns a list of the users created playlists.'''
        result_list = []
        current_user_id = self.spotify.current_user()["id"]

        # fetch all playlists
        done = False
        offset = 0

        # iterate over playlist collection
        while not done:
            results = self.spotify.current_user_playlists(limit=50,offset=offset)

            if len(results["items"]) < 50:
                done = True

            for item in results["items"]:
                if item["owner"]["id"] == current_user_id:
                    result_list.append(objects.playlist.Playlist(id=item["id"], name=item["name"], owner_id=current_user_id))

        return result_list

    def add_genres(self, artist: objects.artist.Artist) -> objects.artist.Artist:
        '''adds genres to artist object'''
        result = self.spotify.artist(artist.get_id())
        artist.set_genres = result["genres"]
        return artist

    
    def test(self):
        print(self.spotify.artist(""))