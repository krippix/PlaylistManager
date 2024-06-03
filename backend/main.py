"""
Main module for Gustelfy backend.
"""
from backend.util import config
from backend.util import database
from backend import auth

import fastapi.middleware.cors

# Starting api
app = fastapi.FastAPI()

db = database.Database()

# retrieve configuration
app.env_dict = config.retrieve_config()


# Needed for cors support
#app.add_middleware(
#    fastapi.middleware.cors.CORSMiddleware,
#    allow_origins=['*'],
#    allow_methods=["*"],
#    allow_headers=["*"]
#)

# add routes within the application
app.include_router(auth.router, prefix="/auth")
