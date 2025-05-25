# external
import pydantic
import fastapi
import fastapi.middleware.cors
import spotipy
# python native
import logging
import sys
# project
from Gustelfy import spotify_api, session
from Gustelfy import database
from Gustelfy.objects import album, artist, playlist, track, user
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


# Starting api
app = fastapi.FastAPI()


# Needed for cors support
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)


# init db
logger.info("Initializing database.")
db_con = database.Database()
db_con.check()


# spotify db
spotify = spotify_api.Spotify_api()


#
# Locations 
# 

@app.get("/")
async def amogus():
    """Gets new key for a new user
    Returns:
        {key:value}    
    """
    return {"amogus" : "sus"}

"""
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
"""

if __name__ == "__main__":
    uvicorn.run(
        app       = "main:app",
        log_level = logging.DEBUG,
        reload    = True
    )