# external
import spotipy
# python native
import logging
import time
# project
from Gustelfy.util import config
from Gustelfy.objects import album, artist, playlist, track, user


class Spotify_api:
    """Class handling the spotify connection
    """

    spotify: spotipy.Spotify
    settings: config.Config
    client_id: str
    client_secret: str
    scopes = [
            "user-library-read",
            "user-library-modify",
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-read-collaborative",
            "playlist-modify-public"
        ]

    def __init__(self):
        # fetch credentials from config.ini
        self.logger = logging.getLogger(__name__)
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
        return self.spotify.current_user()["id"]


    def get_display_name(self) -> str:
        '''returns current user's display name.'''
        return self.spotify.current_user()["display_name"]
    
    # ---- Setter Functions ----

    # ---- Other Functions ----

    # -- Fetch --

    def fetch_track(self, track_id: str) -> track.Track:
        """Fetches detailed track information from Spotify database, rudimentary artist and album information.

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

        # add artists ids into list
        artists = []
        for curr_artist in result["artists"]:
            artists.append(artist.Artist(id=curr_artist["id"], name=curr_artist["name"]))

        # Album
        # Album artists
        album_artists = []
        for album_artist in result["album"]["artists"]:
            album_artists.append(artist.Artist(id=album_artist["id"],name=album_artist["name"]))

        # Build album to append
        tr_album = album.Album(
            id=result["album"]["id"],
            name=result["album"]["name"],
            artists=artists,
            total_tracks=result["album"]["total_tracks"],
        )
        result_track = track.Track(
            id=track_id,
            name=result["name"],
            artists=artists,
            duration_ms=result["duration_ms"],
            album=tr_album,
            disc_number=result["disc_number"],
            tracK_number=result["track_number"],
            explicit=result["explicit"],
            popularity=result["popularity"]
        )
        
        return track.Track(id=track_id, name=result["name"], artists=artists, timestamp=int(time.time()))
    

    def fetch_favorites(self) -> list[track.Track]:
        '''Takes all tracks from users favorites and returns them as List of track objects'''
        result_list = []

        # fetch favorites
        done = False
        offset = 0

        # iterate over favorites
        while not done:
            results = self.spotify.current_user_saved_tracks(limit=50,offset=offset)

            if len(results["items"]) < 50:
                done = True
            
            for song in results["items"]:
                song = song["track"]
                
                # put artists into one list
                artists = []
                for curr_artist in song["artists"]:
                    artists.append(artist.Artist(curr_artist["id"],curr_artist["name"], timestamp=int(time.time())))
                
                result_list.append(track.Track(id=song["id"],name=song["name"],artists=artists, timestamp=int(time.time())))
            offset += 50
        
        return result_list


    def fetch_playlists(self) -> list[playlist.Playlist]:
        '''Returns a list of the users created playlists.'''
        self.logger.debug(f"fetch_playlists()")
        
        result_list = []
        current_user_id = self.spotify.current_user()["id"]

        # fetch all playlists
        done = False
        offset = 0

        # iterate over playlist collection
        while not done:
            results = self.spotify.current_user_playlists(limit=50,offset=offset)

            if len(results["items"]) < 50:
                done = True

            for item in results["items"]:
                if item["owner"]["id"] == current_user_id:
                    result_list.append(playlist.Playlist(id=item["id"], name=item["name"], owner_id=current_user_id))

        return result_list

    
    def fetch_playlist_songs(self, playlist_id: str) -> list[track.Track]:
        '''Returns list of songs in given playlist.'''
        self.logger.debug(f"fetch_playist_songs({playlist_id})")
        
        tracks = []

        api_result = self.spotify.playlist_tracks(playlist_id=playlist_id)

        for track in api_result["item"]:
            # Handle artists in track
            artists = []
            for artist in track["track"]["artists"]:
                artists.append(artist.Artist(id=artist["id"],name=artist["name"],timestamp=int(time.time())))
            # Create final track object
            tracks.append(track.Track(id=track["track"]["id"],name=track["track"]["name"],artists=artists,timestamp=int(time.time())))
        
        return tracks


    def add_genres(self, artist: artist.Artist) -> artist.Artist:
        '''adds genres to artist object'''
        result = self.spotify.artist(artist.get_id())
        artist.set_genres = result["genres"]
        return artist


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()