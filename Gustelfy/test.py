# external
# python native
import time, logging, json
# project
from Gustelfy import database
from Gustelfy.objects import album, artist, playlist, track, user
from Gustelfy.util import config
from Gustelfy import session, spotify_api

def test():
    """Testrun without flask"""
    logger = logging.getLogger(__name__)
    
    ##testalbum = album.Album("amogus", "amogus", [track.Track("amo_gus", "name", [artist.Artist("i","i",12)])], [artist.Artist("i","i",12)])

    # Initialise config object
    settings = config.Config()
    
    # Connect to database and fix table
    db = database.Database("oracledb").get_db_connection()

    # Create spotify testuser
    usr = user.User("testmanfred")

    # Connect to spotify
    spotify = spotify_api.Spotify_api()

    user_session = session.Session(usr, spotify, db)
    #data = user_session.get_homepage_data()
    #user_session.commit_favorites_changes(data["changes"])

    user_session.commit_favorites_changes(user_session.get_favorites_changes())

def api():
    logger = logging.getLogger(__name__)
    settings = config.Config()
    spotify = spotify_api.Spotify_api()
    result = {}
    
    # Turbo thomas: 2vWnOXI1ALzlvNTdjVPMG1
    # Rap über hass: 21ownMQ51Jqlv8si9CTI6R
    #result = spotify.fetch_track('21ownMQ51Jqlv8si9CTI6R')
    #result = spotify.fetch_album("1kTlYbs28MXw7hwO0NLYif")
    #result = spotify.fetch_artist("7cHFXNgK44YndrHbEQWsZR")
    result = spotify.fetch_playlist("349T3IRkkkTyBc1SqyP1JH",json=True)
    with open('test.json', 'w') as amogus:
        json.dump(result,amogus,indent=3)
    result = spotify.fetch_playlist("349T3IRkkkTyBc1SqyP1JH",json=False)
    print(result.get_tracks())

"""
    result = spotify.test("349T3IRkkkTyBc1SqyP1JH")
    with open('test_playlist_track.json', 'w') as amogus:
        json.dump(result,amogus,indent=3)
"""

def db_connection():
    "pyhton -m Gustelfy db"
    db = database.Database("oracledb").get_db_connection()
    db.connect_database()
    
    test_artist = artist.Artist(
        id="42069",
        name="Arschbach Poposohn",
        genres=["wurst and roll","rap"]
    )
    test_artist.set_image_url("https://google.com/image/amogus.png")
    
    #result = db.get_artist("42069")
    #print(result.get_genres())
    print(db.add_artist(test_artist))

    #db.add_artist(test_artist)