# external
# python native
import time
# project
from Gustelfy.database import database
from Gustelfy.objects import album, artist, playlist, track, user
from Gustelfy.util import config


def test():
    """Testrun without flask"""
    logger = logging.getLogger(__name__)
    
    ##testalbum = album.Album("amogus", "amogus", [track.Track("amo_gus", "name", [artist.Artist("i","i",12)])], [artist.Artist("i","i",12)])

    # Check config for errors
    settings = config.Config()
    settings.checkConfig()
    
    # Connect to database and fix table
    logger.info("Establishing database connection.")
    db = database.Database("sqlite3").get_db_connection()
    db.check()

    # Connect to spotify
    spotify = spotify_api.Spotify_api()

    user_session = session.Session(spotify, db)
    data = user_session.get_homepage_data()
    user_session.commit_favorites_changes(data["changes"])

def db_connection():
    "pyhton -m Gustelfy db"
    db = database.Database("oracledb").get_db_connection()
    db.connect_database()
    
    test_artist = artist.Artist(
        id="42069",
        name="Arbasch Poposohn",
        genres=["wurst and roll","rap"]
    )
    test_artist.set_image_url("https://google.com/image/amogus.png")
    
    #result = db.get_artist("42069")
    #print(result.get_genres())
    print(db.add_artist(test_artist))

    #db.add_artist(test_artist)