# external
import flask
import spotipy
# python native
import logging
import sys
# project
from Gustelfy import spotify_api, session
from Gustelfy.database import database
from Gustelfy.objects import track, playlist, album
from Gustelfy.util import config

# prepare project configuration
settings = config.Config()
settings.checkConfig()

# Logging config
logger = logging.getLogger(__name__)
try:
    logger.setLevel(settings.get_loglevel())
except:
    logger.setLevel(logging.DEBUG)


# Flask configuration
app = flask.Flask(__name__, root_path=settings.folders["root"], template_folder=settings.folders["templates"])


@app.before_first_request
def before_first_request():
    logger.info("Initializing database.")
    db_con = database.Database()
    db_con.ensure_default_tables()
    # spotify api connection
    spotify = spotify_api.Spotify_api()


@app.route('/', methods=('GET','POST'))
def index():
    print(flask.request.method)
    if flask.request.method == 'POST':
        print(f"Found keys: {flask.request.form}")
        
    # Database init
    db_con = database.Database()
    spotify = spotify_api.Spotify_api()
    #spotify.add_genres(objects.artist.Artist("7dGJo4pcD2V6oG8kP0tJRR", "Eminem"))
    #track = spotify.fetch_track_artists(spotify.fetch_track("7lQ8MOhq6IN2w8EYcFNSUk"))

    #print(track.get_name())
    #print(track.get_artists())
    #print(track.get_artists()[0].get_genres())
    user_session = session.Session(spotify, db_con)
    user_session.update_library()
    data = user_session.get_homepage_data()
    user_session.commit_library_changes(data["changes"])
    
    return flask.render_template('index.html', dict=data)


def test():
    """Testrun without flask"""
    logger = logging.getLogger(__name__)
    
    # Check config for errors
    settings = config.Config()
    settings.checkConfig()
    
    # Connect to database and fix table
    logger.info("Establishing database connection.")
    db = database.Database("sqlite3").get_db_connection()
    db.check()


if __name__ == "__main__":    
    try:
        if sys.argv[1] == "testrun":
            test()
    except Exception as e:
        logger.error("This is a flask application, start it with 'flask run'")
        exit()