import logging
from util import config
import util.database as database
import download
import spotipy

def main():
    ''''''
    # prepare project configuration
    settings = config.Config()

    # Database init
    db_con = database.Database(settings)
    
    # fetch credentials from config.ini
    missing_credentials = False
    client_id = settings.get_config("AUTH","client_id")
    client_secret = settings.get_config("AUTH","client_secret")
    
    if len(client_id) == 0:
        logging.critical("No client id has been provided, please add one to data/config.ini")
        missing_credentials = True
    if len(client_secret) == 0:
        logging.critical("No client secret has been provided, please add one to data/config.ini")
        missing_credentials = True
    
    if missing_credentials:
        logging.info("Exiting software.")
        exit()
    
    # Authorize Application and user with Spotify
    scopes = [
        "user-library-read",
        "user-library-modify",
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-read-collaborative",
        "playlist-modify-public"
    ]
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scopes,
        client_id=client_id,
        client_secret=client_secret,
        #open_browser=False,
        #show_dialog=True,
        redirect_uri="http://172.0.0.1:9090"
    )
    
    # Get Auth URL where user has to login and confirm
    #auth_manager.
    #print(auth_manager.get_authorize_url())

    # connect to spotify
    connection = spotipy.Spotify(auth_manager=auth_manager)

    # Test Print user tracks
    #print(connection.current_user())
    #print(connection.user())
    
    list = download.fetch_library(connection)
    print(list[0])
    
    

if __name__ == "__main__":
    main()