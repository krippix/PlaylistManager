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
        self.logger = logging.getLogger("Gustelfy.spotify_api")
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
            self.logger.critical("No client id has been provided, please add one to data/config.ini")
            missing_credentials = True
        if len(self.client_secret) == 0:
            self.logger.critical("No client secret has been provided, please add one to data/config.ini")
            missing_credentials = True
        
        if missing_credentials:
            self.logger.info("Exiting software.")
            exit()


    ############
    # get
    ############

    def get_connection(self) -> spotipy.Spotify:
        '''Returns spotify API connection object.'''
        return self.spotify
    

    def get_user_id(self) -> str:
        '''Returns current user's spotify id.'''
        return self.spotify.current_user()["id"]


    def get_display_name(self) -> str:
        '''returns current user's display name.'''
        return self.spotify.current_user()["display_name"]
    

    def fetch_track(self, track: objects.track.Track | str):
        '''Pulls track from spotify api by id. Including rudimentary artist information'''
        self.logger.debug(f"fetch_track({track})")
        
        if isinstance(track, str):
            id = track
        else:
            id = track.get_id()
            
        result = self.spotify.track(track_id=id)

        if result is None:
            # TODO might need error handling here
            self.logger.error("Track not found in spotify db.")
            return None

        # add artists ids into list
        artists = []
        for artist in result["artists"]:
            artists.append(objects.artist.Artist(id=artist["id"], name=artist["name"], timestamp=int(time.time())))

        return objects.track.Track(id=track.get_id(), name=result["name"], artists=artists, timestamp=int(time.time()))
    

    def fetch_library(self) -> list[objects.track.Track]:
        '''Takes all tracks from users library and returns them as List of track objects'''
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


    def fetch_playlists(self) -> list[objects.playlist.Playlist]:
        '''Returns a list of the users created playlists.'''
        self.logger.debug(f"fetch_playlists()")
        
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

    
    def fetch_playlist_songs(self, playlist_id: str) -> list[objects.track.Track]:
        '''Returns list of songs in given playlist.'''
        self.logger.debug(f"fetch_playist_songs({playlist_id})")
        
        tracks = []

        api_result = self.spotify.playlist_tracks(playlist_id=playlist_id)

        for track in api_result["item"]:
            # Handle artists in track
            artists = []
            for artist in track["track"]["artists"]:
                artists.append(objects.artist.Artist(id=artist["id"],name=artist["name"],timestamp=int(time.time())))
            # Create final track object
            tracks.append(objects.track.Track(id=track["track"]["id"],name=track["track"]["name"],artists=artists,timestamp=int(time.time())))
        
        return tracks


    def add_genres(self, artist: objects.artist.Artist) -> objects.artist.Artist:
        '''adds genres to artist object'''
        result = self.spotify.artist(artist.get_id())
        artist.set_genres = result["genres"]
        return artist


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()