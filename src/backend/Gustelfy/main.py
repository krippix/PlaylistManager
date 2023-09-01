# external
import pydantic
import fastapi
import fastapi.middleware.cors
import spotipy
import uvicorn
# python native
import logging 
import sys
# project
import database, spotify_api, session
from objects import album, artist, playlist, track, user
from util import config


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

if __name__ == "__main__":
    uvicorn.run(
        app       = "main:app",
        log_level = logging.DEBUG,
        reload    = True
    )