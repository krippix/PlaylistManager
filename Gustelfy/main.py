# external
import uvicorn
import pydantic
import fastapi
import fastapi.middleware.cors
import spotipy
# python native
import logging
import sys
# project
from Gustelfy import spotify_api, database, session, basemodels
from Gustelfy.objects import artist, playlist, track, user
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


@app.get("/playlists")
async def get_playlists(user_id: str):
    """Returns playlists the user owns

    Returns:
        _description_
    """
    u_session = session.Session(user_id, spotify, db_con)
    playlists_dict = [x.as_dict() for x in u_session.get_playlists()]
    return playlists_dict


@app.get("/update")
async def update(user_id: str):
    """Updates local data of the user and updates playlists

    Args:
        user_id: _description_

    Returns:
        _description_
    """


@app.get("/favorite_diff")
async def favorite_diff(user_id: str):
    """Returns changes of the users favorites
    """
    usr_session = session.Session(user_id, spotify, db_con)

    data = usr_session.get_favorites_changes()
    added   = [x.as_dict() for x in data[0]]
    removed = [x.as_dict() for x in data[1]]

    return {"added":added, "removed":removed}


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

def run():
    uvicorn.run(
        app       = "main:app",
        log_level = logging.DEBUG,
        reload    = True
    )

if __name__ == "__main__":
    run()