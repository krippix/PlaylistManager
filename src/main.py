import logging
from util import config
import spotipy

def main():
    ''''''
    # prepare project configuration
    settings = config.Config()
    scopes = "user-library-modify playlist-modify-private"

    client_id = settings.get_config("AUTH","client_id")
    client_secret = settings.get_config("AUTH","client_secret")

    # connect to spotify
    connection = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope=scopes,client_id=client_id,client_secret=client_secret,redirect_uri="http://172.0.0.1"))













if __name__ == "__main__":
    main()