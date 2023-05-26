# external
import spotipy
from spotipy import CacheHandler
from requests import ReadTimeout
# python native
import logging
import time
# project
from Gustelfy import database
from Gustelfy.util import config
from Gustelfy.objects import artist, playlist, track, user


class Spotify_api:
    """Class handling the spotify connection
    """
    spotify: spotipy.Spotify
    settings: config.Config
    user: user.User
    client_id: str
    client_secret: str
    scopes = [
            "user-library-modify",
            "user-library-read",
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-read-collaborative",
            "playlist-modify-public"
        ]

    def __init__(self, user=None):
        # fetch credentials from config.ini
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"__init__()")
        self.settings = config.Config()
        self.client_id = self.settings.get_config("AUTH","client_id")
        self.client_secret = self.settings.get_config("AUTH","client_secret")

        # Authorize Application and user with Spotify
        
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=self.scopes,
            client_id=self.client_id,
            client_secret=self.client_secret,
            #open_browser=False,
            #show_dialog=True,
            redirect_uri="http://172.0.0.1:9090"
        )

        # connect to spotify
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)

    def check_credentials(self):
        '''Checks if any credentials have been provided in config.ini'''
        self.logger.debug(f"check_credentials()")
        missing_credentials = False
        
        if len(self.client_id) == 0:
            self.logger.critical("No client id has been provided, please add one to data/config.ini")
            missing_credentials = True
        if len(self.client_secret) == 0:
            self.logger.critical("No client secret has been provided, please add one to data/config.ini")
            missing_credentials = True
        
        if missing_credentials:
            self.logger.info("Exiting software.")
            exit()

    # ---- Getter Functions ----

    def get_connection(self) -> spotipy.Spotify:
        '''Returns spotify API connection object.'''
        return self.spotify
    

    def get_user_id(self) -> str:
        '''Returns current user's spotify id.'''
        retry = 0
        while True:
            try:
                return self.spotify.current_user()["id"]
            except ReadTimeout as e:
                time.sleep(1+2*retry)
                retry += 1
                if retry > 4:
                    raise e


    def get_display_name(self) -> str:
        '''returns current user's display name.'''
        return self.spotify.current_user()["display_name"]
    
    # ---- Setter Functions ----

    # ---- Other Functions ----

    # -- Fetch --
    
    def fetch_artist(self, artist_id: str, json=False) -> artist.Artist:
        self.logger.debug(f"fetch_artist({artist_id})")
        try:
            result = self.spotify.artist(artist_id)
        except Exception as e:
            self.logger.error(f"Artist with id '{artist_id}' not found.\n{e}")
            return None
        if json:
            return result
        # Get Genres
        genre_list = []
        for gnr in result["genres"]:
            genre_list.append(gnr)
        # Create artist object
        artist_result = artist.Artist(
            id=artist_id,
            name=result["name"],
            genres=genre_list,
            images=result["images"],
            popularity=result["popularity"],
            followers=result["followers"]["total"]
        )
        return artist_result

    def fetch_playlists(self, json=False) -> list[playlist.Playlist]:
        """Returns useres **owned** playlists

        Args:
            json (bool, optional): Returns json result. Defaults to False.

        Returns:
            list[playlist.Playlist]: list of playlists
        """
        self.logger.debug(f"fetch_playlists()")

        user_id = self.get_user_id()

        # Return raw json
        if json:
            return self.spotify.current_user_playlists(limit=50,offset=0)

        # fetch all playlists
        done = False
        offset = 0
        valid_lists = 0
        playlist_list = []
        while not done:
            results = self.spotify.current_user_playlists(limit=50,offset=offset)
            valid_lists = results["total"]
            # Append Playlists
            for lst in results["items"]:
                if lst["owner"]["id"] == user_id:
                    playlist_list.append(playlist.Playlist(
                        id   = lst["id"],
                        name = lst["name"]
                    ))
                else:
                    valid_lists -= 1
            if len(playlist_list) >= valid_lists:
                done = True
            offset += 50
        return playlist_list

    def fetch_playlist(self, playlist_id: str,json=False) -> playlist.Playlist:
        """Returns Playlist and it's songs

        Args:
            playlist_id (str): Spotify Playlist id
            json (bool, optional): Returns raw api result. Defaults to False.

        Returns:
            playlist.Playlist: _description_
        """
        self.logger.debug(f"fetch_playlist({playlist_id})")
        try:
            result = self.spotify.playlist(playlist_id)
        except Exception as e:
            self.logger.error(f"Playlist with id '{playlist_id}' not found.\n{e}")
            return None
        if json:
            return result
        # Get tracks seperately, because they contain more details that way
        playlist_tracks = self.fetch_playlist_tracks(playlist_id)
        try:
            playlist_result = playlist.Playlist(
                id          = playlist_id,
                name        = result["name"],
                tracks      = playlist_tracks
            )
        except Exception as e:
            print(result)
            print(f"Bruh wtf: {e}")
        return playlist_result

    def fetch_playlist_tracks(self, playlist_id: str, json=False) -> list[track.Track]:
        """Gets detailed playlist track information

        Args:
            playlist_id (str): _description_

        Returns:
            list[track.Track]: _description_
        """
        self.logger.debug(f"__fetch_playlist_tracks({playlist_id}, {json})")
        if json:
            return self.spotify.playlist_tracks(playlist_id)
        done = False
        offset = 0
        track_list = []
        while not done:            
            result = self.spotify.playlist_tracks(playlist_id,offset=offset)

            for item in result["items"]:
                # I have no clue why this can happen, but it does
                if item["track"] is None:
                    result["total"] -= 1
                    continue
                # Get track artists
                track_artists = []
                for art in item["track"]["artists"]:
                    track_artists.append(artist.Artist(
                        id   = art["id"],
                        name = art["name"]
                    ))
                track_list.append(track.Track(
                    id      = item["track"]["id"],
                    name    = item["track"]["name"],
                    artists = track_artists
                ))
            if len(track_list) == result["total"]:
                done = True
            else:
                offset += 100
        return track_list
    
    def fetch_track(self, track_id: str, json=False) -> track.Track:
        """Fetches detailed track information from Spotify database, rudimentary artist information.

        Args:
            track_id (str): _description_

        Returns:
            _type_: _description_
        """
        self.logger.debug(f"fetch_track({track_id})")
        try:
            result = self.spotify.track(track_id=track_id)
        except Exception as e:
            logging.error(f"Track with id '{track_id}' not found.\n{e}")
            return None
        if json:
            return result

        # add artists ids into list
        artists = []
        for curr_artist in result["artists"]:
            artists.append(artist.Artist(id=curr_artist["id"], name=curr_artist["name"]))

        result_track = track.Track(
            id      = track_id,
            name    = result["name"],
            artists = artists
        ) 
        return result_track
    
    def fetch_favorites(self, json=False) -> list[track.Track]:
        """Get list of favorites a user has aquired

        Args:
            json (bool, optional): return raw json instead of a spotify object. Defaults to False.

        Returns:
            list[track.Track]: _description_
        """
        # json result for debugging
        if json:
            return self.spotify.current_user_saved_tracks(limit=50)

        # fetch favorites
        done       = False
        offset     = 0
        track_list = []

        while not done:
            results = self.spotify.current_user_saved_tracks(limit=50,offset=offset)
            for trk in results["items"]:
                # get track artists
                trk_artists = []
                for art in trk["track"]["artists"]:
                    trk_artists.append(artist.Artist(
                        id   = art["id"],
                        name = art["name"]
                    ))
                # create track object
                track_list.append(track.Track(
                    id      = trk["track"]["id"],
                    name    = trk["track"]["name"],
                    artists = trk_artists
                ))
            if offset >= results["total"]:
                done = True
            else:
                offset += 50
        return track_list
    
    def fetch_current_user(self, json=False) -> user.User:
        """Returns detailed spotify user object.

        Returns:
            user.User: _description_
        """
        result = self.spotify.current_user()
        if json:
            return result
        user_result = user.User(
            id=result["id"],
            display_name=result["display_name"],
            image_url=result["images"][0]["url"],
            followers=result["followers"]["total"]
        )
        return user_result

class CacheDatabaseHandler(CacheHandler):
    """
    Implements CacheHandler for using SQL databases
    """
    def __init__(self, database: database.Database, user_id: str):
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.user_id = user_id
        

    def get_cached_token(self):
        token_info = None
        try:
            token_info = self.database.get_token(self.user_id)
        except Exception as e:
            self.logger.error(f"Failed to retrieve API token for user: {e}")
        return token_info
    
    def save_token_to_cache(self, token_info):
        self.database.set_token(self.user_id,token_info)
    
    
if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()