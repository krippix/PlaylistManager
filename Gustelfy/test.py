# external
# python native
import time
import logging
import json
import sys
import winsound
import traceback
# project
from Gustelfy import database
from Gustelfy.objects import artist, playlist, track, user
from Gustelfy.util import config
from Gustelfy import session, spotify_api


def test():
    try:
        if len(sys.argv) >= 2:
            if sys.argv[2] == "api":
                api()
            if sys.argv[2] == "merge":
                merge()
            if sys.argv[2] == "db":
                db_connection()
            if sys.argv[2] == "dbp":
                dbp()
            if sys.argv[2] == "obj":
                objects()
            if sys.argv[2] == "update":
                db_update()
        else:
            print("Select test to run.")
    except Exception as e:
        print(e)
        traceback.print_exc()
        amogus()
        exit()
    winsound.Beep(523, 300) # C5
    winsound.Beep(523, 150) # C5
    winsound.Beep(659, 600) # E5


def db_update():
    """Testing update of incomplete entries
    """
    logger = logging.getLogger("Gustelfy")
    logger.setLevel(10)
    logger.debug("amogus")
    session = prepare()

    session.update_database()


def dbp():
    """Testrun without flask"""
    logger = logging.getLogger("Gustelfy")
    logger.setLevel(10)
    # Initialise config object
    settings = config.Config()
    # Connect to database and fix table
    db = database.Database("oracledb").get_db_connection()
    usr = user.User("testmanfred")
    # Connect to spotify
    spotify = spotify_api.Spotify_api()
    user_session = session.Session(usr, spotify, db)

    # Test database fillup
    user_session.dbp_fill_db()


def objects():
    """testing different objects"""
    user_session = prepare()

    #
    test_artist = artist.Artist(
        id         = "11111_test",
        name       = "11111_test",
        genres     = ["test_genre1","test_genre2"],
        images     = [{"height":64,"url":"https://www.scdn.co/i/_global/favicon.png","width":64}],
        popularity = 69,
        followers  = 420
    )

    test_track = track.Track(
        id           = "11111_test",
        name         = "TEST_TRACK",
        artists      = [test_artist]
    )

    #user_session.db_con.add_artist(test_artist)
    user_session.db_con.add_track(test_track)
    return


def api():
    logger = logging.getLogger("Gustelfy")
    logger.setLevel(10)
    settings = config.Config()
    spotify = spotify_api.Spotify_api()
    result = {}
    
    # Turbo thomas: 2vWnOXI1ALzlvNTdjVPMG1
    # Rap über hass: 21ownMQ51Jqlv8si9CTI6R
    #result = spotify.fetch_track('21ownMQ51Jqlv8si9CTI6R',json=True)
    result = spotify.fetch_artist("1ehBmvzykgp3Il0BUIZdev",json=True)
    result_o = spotify.fetch_artist("1ehBmvzykgp3Il0BUIZdev")
    #result = spotify.fetch_playlist("349T3IRkkkTyBc1SqyP1JH",json=True)
    #result = spotify.fetch_playlist("5JfpaSo0hvoRdGRYFrEP3x",json=True) # wtf?
    #result = spotify.amogus("5JfpaSo0hvoRdGRYFrEP3x")
    #result = spotify.fetch_favorites(json=True)
    #result = spotify.fetch_playlists(json=True)
    #result = spotify.fetch_user(json=True)
    #result = spotify.fetch_playlist_tracks("349T3IRkkkTyBc1SqyP1JH",json=True)
    print(result_o.get_followers())
    with open('test.json', 'w') as amogus:
        json.dump(result,amogus,indent=3)
        print("result written to test.json")
    #result = spotify.fetch_playlist("349T3IRkkkTyBc1SqyP1JH")
    #print(result.get_tracks())


def merge():
    """Testing the merge function for different spotify objects
    """
    old = track.Track(
        id="amogus123",
        artists=[],
        name="Amogus Party",
        timestamp=1,
        duration_ms=12343,
        explicit=False,
        popularity=20,
        track_number=12
    )
    new = track.Track(
        id="amogus123",
        artists=[artist.Artist(id="mogusmann",name="kekw")],
        name="Amogus Party",
        timestamp=3,
        duration_ms=123,
        explicit=True,
        popularity=20
    )
    new.merge(old)
    mogus = new
    print(
        f"{mogus.get_id()} {mogus.get_artists()} {mogus.get_name()} {mogus.get_timestamp()} {mogus.get_duration_ms()} {mogus.is_expired()} {mogus.get_popularity()} {mogus.get_track_number()}"
    )


def amogus():
    """sus
    """
    winsound.Beep(523, 300) # C5
    winsound.Beep(622, 300) # E5 flat
    winsound.Beep(698, 300) # F5
    winsound.Beep(740, 300) # G5 flat
    winsound.Beep(698, 300) # F5
    winsound.Beep(622, 300) # E5 flat
    winsound.Beep(523, 300) # C5
    time.sleep(0.6)
    winsound.Beep(466, 150) # B4 flat
    winsound.Beep(587, 150) # D5
    winsound.Beep(523, 300) # C5


def prepare() -> session.Session:
    logger = logging.getLogger("Gustelfy")
    logger.setLevel(10)
    # Initialise config object
    config.Config()
    # Connect to database and fix table
    db = database.Database("oracledb").get_db_connection()
    usr = user.User("testmanfred")
    # Connect to spotify
    spotify = spotify_api.Spotify_api()
    return session.Session(usr, spotify, db)


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