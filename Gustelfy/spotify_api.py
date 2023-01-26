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

    def fetch_album(self, album_id: str) -> album.Album:
        self.logger.debug(f"fetch_album({album_id})")
        try:
            result = self.spotify.album(album_id)
        except Exception as e:
            logging.error(f"Album with id '{album_id}' not found.\n{e}")
            return None
    
        # get artists
        artist_list = []
        for art in result["artists"]:
            artist_list.append(artist.Artist(id=art["id"],name=art["name"]))

        # get images
        image_list = []
        for img in result["images"]:
            image_list.append((img["height"],img["url"],img["width"]))
        
        # get Tracks
        # TODO: handle more than 50 tracks in single album
        album_tracks = []
        for trk in result["tracks"]["items"]:
            # Add track artists
            trk_artists = []
            for trk_art in trk["artists"]:
                trk_artists.append(artist.Artist(id=trk_art["id"],name=trk_art["name"]))
            album_tracks.append(track.Track(
                id=trk["id"],
                name=trk["name"],
                artists=trk_artists,
                disc_number=trk["disc_number"],
                duration_ms=trk["duration_ms"],
                explicit=trk["explicit"],
                track_number=trk["track_number"]
            ))
        # Build album object
        result_album = album.Album(
            id=album_id,
            artists=artist_list,
            images=image_list,
            name=result["name"],
            popularity=result["popularity"],
            release_date=result["release_date"],
            total_tracks=result["total_tracks"]
        )
        return result_album
    
    def fetch_artist(self, artist_id: str) -> artist.Artist:
        self.logger.debug(f"fetch_artist({artist_id})")
        try:
            result = self.spotify.artist(artist_id)
        except Exception as e:
            self.logger.error(f"Artist with id '{artist_id}' not found.\n{e}")
            return None
        # Get images
        img_list = []
        for img in result["images"]:
            img_list.append((img["height"],img["url"],img["width"]))
        # Get Genres
        genre_list = []
        for gnr in result["genres"]:
            genre_list.append(gnr)
        # Create artist object
        artist_result = artist.Artist(
            id=artist_id,
            name=result["name"],
            genres=genre_list,
            images=img_list,
            popularity=result["popularity"],
            followers=result["followers"]["total"]
        )
        return artist_result

    def fetch_playlist(self, playlist_id: str,json=False) -> playlist.Playlist:
        self.logger.debug(f"fetch_playlist({playlist_id})")
        try:
            result = self.spotify.playlist(playlist_id)
        except Exception as e:
            self.logger.error(f"Playlist with id '{playlist_id}' not found.\n{e}")
            return None
        if json:
            return result
        # Get tracks seperately, because they contain more details that way
        playlist_tracks = self.__fetch_playlist_tracks(playlist_id)
        
        playlist_result = playlist.Playlist(
            id=playlist_id,
            name=result["name"],
            creator_id=result["owner"]["id"],
            tracks=playlist_tracks,
            description=result["description"],
            image_url=result["images"][0]["url"],
        )
        return playlist_result

    def __fetch_playlist_tracks(self, playlist_id: str) -> list[track.Track]:
        result = self.spotify.playlist_tracks(playlist_id)
        track_list = []
        for item in result["items"]:
            # Get track artists
            track_artists = []
            for art in item["track"]["artists"]:
                track_artists.append(artist.Artist(
                    id=art["id"],
                    name=art["name"]
                ))
            # Get album artists
            album_artists = []
            for art in item["track"]["album"]["artists"]:
                album_artists.append(artist.Artist(
                    id=art["id"],
                    name=art["name"]
                ))
            # Get track album
            track_album = album.Album(
                id=item["track"]["album"]["id"],
                name=item["track"]["album"]["name"],
                artists=album_artists
            )
            track_list.append(track.Track(
                id=item["track"]["id"],
                name=item["track"]["name"],
                artists=track_artists,
                duration_ms=item["track"]["duration_ms"],
                album=track_album,
                disc_number=item["track"]["disc_number"],
                track_number=item["track"]["track_number"],
                explicit=item["track"]["explicit"],
                popularity=item["track"]["popularity"]
            ))
        return track_list

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

        # Create album images
        album_image_list = []
        for image in result["album"]["images"]:
            album_image_list.append((image["height"],image["url"],image["width"]))

        # Build album to append
        tr_album = album.Album(
            id=result["album"]["id"],
            name=result["album"]["name"],
            artists=artists,
            total_tracks=result["album"]["total_tracks"],
            images=album_image_list
        )
        result_track = track.Track(
            id=track_id,
            name=result["name"],
            artists=artists,
            duration_ms=result["duration_ms"],
            album=tr_album,
            disc_number=result["disc_number"],
            track_number=result["track_number"],
            explicit=result["explicit"],
            popularity=result["popularity"]
        ) 
        return result_track
    
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