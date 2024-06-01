"""
This file handles all configuration options within this project.
"""
from backend.util.database import Database

import os

# Database object to be used all over the project
database = Database()


def retrieve_config() -> dict:
    """
    Retrieves config parameters from environment variables.
    Exits software if any are missing.
    """
    required_keys = [
        "SPOTIPY_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET",
        "SPOTIPY_REDIRECT_URI",
    ]
    optional_keys = [
    ]
    result_dict = {key: os.environ.get(key, None) for key in required_keys}

    failed_keys = [key for key, value in result_dict.items() if value is None]

    result_dict.update({key: os.environ.get(key, None) for key in optional_keys})

    if failed_keys:
        print(f"The following environment variables are missing: {failed_keys}")
        raise SystemExit(1)
    return result_dict


def get_scopes() -> str:
    scopes = [
        "playlist-read-private",
        "playlist-modify-private",
        "user-library-modify",
    ]
    return ",".join(scopes)
