# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import track

class Playlist(spotifyObject.SpotifyObject):
    
    creator_id: str
    managed: bool
    tracks = []
    description: str
    image_url: str
    genres: list[str]
    
    def __init__(self, 
                id: str, 
                name: str,
                user_id: str,
                creator_id: str,
                tracks=[],
                managed=0,
                timestamp=int(time.time()),
                description="",
                image_url="",
                genres=[]
                ):
        """Creates a Spotify Playlist object

        Args:
            id (str): Spotify ID of the Playlist
            name (str): Playlist (display) name
            user_id (str): Spotify ID of the user following the playlist in this context
            creator_id (str): Spotify ID of the Playlist creator
            tracks (list, optional): tracks within the playlist. Defaults to [].
            managed (int, optional): Whether or not the playlist will be managed by this software. Defaults to 0.
            timestamp (int, optional): timestamp integer. Defaults to int(time.time()).
            image_url (str, optional): Playlist image url. Defaults to "".
            genres (list, optional): List of genres to be auto-included. Defaults to [].
        """
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_user_id(user_id)
        self.set_creator_id(creator_id)
        self.set_tracks(tracks)
        self.set_managed(managed)
        self.set_description(description)
        self.set_image_url(image_url)
        self.set_genres(genres)

    # ---- Getter Functions ----

    def get_user_id() -> str:
        return self.user_id

    def get_creator_id() -> str:
        return self.creator_id

    def is_managed() -> bool:
        if self.managed:
            return 1
        else:
            return 0

    def get_tracks() -> list[track.Track]:
        return self.tracks

    def get_description() -> str:
        return self.description

    def get_image_url() -> str:
        return self.image_url

    def get_genres() -> list[str]:
        return self.genres

    # ---- Setter Functions ----

    def set_user_id(self, user_id: str):
        self.user_id = user_id

    def set_creator_id(self, creator_id: str):
        self.creator_id = creator_id

    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks

    def set_managed(self, is_managed: bool):
        self.managed = is_managed

    def set_description(self, description: str):
        self.description = description

    def set_image_url(self, url: str):
        self.image_url = url
    
    def set_genres(self, genres: list[str]):
        self.genres = genres

    # ---- Other Functions ----

    def is_equal(self, other: 'Playlist') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Playlist): playlist to compare to

        Returns:
            bool: whether or not they are equal
        """
        if other is None:
            return False
        if self.get_id() != other.get_id():
            return False
        if self.get_name() != other.get_name():
            return False
        if self.get_creator_id() != other.get_creator_id():
            return False
        if self.is_managed() != other.is_managed():
            return False
        
        # Check if songs are the same
        for track in self.get_tracks():
            subresult = False
            for other_track in other.get_tracks():
                if track == other_track:
                    subresult = True
            if subresult == False:
                return False
        return True
