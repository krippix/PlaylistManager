# external
import spotipy
# python native
import logging
# project
import util.config

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