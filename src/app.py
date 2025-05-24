# external
import spotipy, flask
# python native
import logging, os
# project
import util.database, util.config
import objects.artist, objects.track
import gustelify, spotify_api

# prepare project configuration
settings = util.config.Config()
settings.checkConfig()

# Logging config
logging.basicConfig(encoding='utf-8', level=logging.ERROR)

# Flask configuration
app = flask.Flask(__name__, root_path=settings.folders["root"], template_folder=settings.folders["templates"])

@app.before_first_request
def before_first_request():
    print("test")
    db_con = util.database.Database()
    db_con.ensure_default_tables()
    # spotify api connection
    spotify = spotify_api.Spotify_api()


@app.route('/')
def index():
    # Database init
    db_con = util.database.Database()
    spotify = spotify_api.Spotify_api()
    print(spotify.get_track("1tjOClAkdMxDfYPO0xvGbG"))
    library = spotify.fetch_library()
    return flask.render_template('index.html', tracks=library)












# Assuming this will be the user input stuff
#gustelify.




#library = fetch.fetch_library()
#for track in library:
#    db_con.add_track()







if __name__ == "__main__":
    logging.error("This is a flask application, start it with 'flask run'")
    exit()