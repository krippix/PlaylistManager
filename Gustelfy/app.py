# external
import spotipy, flask
# python native
import logging, os
# project
import util
import objects.artist, objects.track
import session, spotify_api

# prepare project configuration
settings = util.config.Config()
settings.checkConfig()

# Logging config
logger = logging.getLogger("Gustelify")
try:
    logger.setLevel(settings.get_config("SCRIPT","loglevel"))
except:
    logger.setLevel(logging.DEBUG)


# Flask configuration
app = flask.Flask(__name__, root_path=settings.folders["root"], template_folder=settings.folders["templates"])

@app.before_first_request
def before_first_request():
    db_con = util.database.Database()
    db_con.ensure_default_tables()
    # spotify api connection
    spotify = spotify_api.Spotify_api()


@app.route('/')
def index():
    # Database init
    db_con = util.database.Database()
    spotify = spotify_api.Spotify_api()
    #spotify.add_genres(objects.artist.Artist("7dGJo4pcD2V6oG8kP0tJRR", "Eminem"))
    #track = spotify.fetch_track_artists(spotify.fetch_track("7lQ8MOhq6IN2w8EYcFNSUk"))

    #print(track.get_name())
    #print(track.get_artists())
    #print(track.get_artists()[0].get_genres())
    test = gustelify.Gustelify(spotify, db_con)

    library = spotify.fetch_library()
    test.add_library()
    

    tmp = [objects.track.Track(id="1234",name="Fick dich",artists=["MC Hurensohn"],timestamp=58),objects.track.Track(id="333",name="Wurstbrotinator",artists=["Brotwurster"],timestamp=58)]
    return flask.render_template('index.html', tracks=tmp)


if __name__ == "__main__":
    logger.error("This is a flask application, start it with 'flask run'")
    
    exit()