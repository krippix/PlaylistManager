import logging, sqlite3
from util import config
import database
import spotipy

def main():
    ''''''
    # prepare project configuration
    settings = config.Config()

    # Database init
    db_con = database.Database(settings)
    db_con.test()
    exit()

    # Authorize Application and user with Spotify
    client_id = settings.get_config("AUTH","client_id")
    client_secret = settings.get_config("AUTH","client_secret")
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
    print(connection.current_user())
    #print(connection.user())
    '''
    results = connection.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    '''

if __name__ == "__main__":
    main()