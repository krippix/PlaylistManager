# external
# python native
import time
# project
from Gustelfy.util import config
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import artist


class Track(spotifyObject.SpotifyObject):
    """Spotify Track object, contains track (song) information
    """

    artists = []
    
    def __init__(self, id: str, name: str, artists: list[artist.Artist], timestamp=int(time.time())):
        '''Creates new artist object with the provided data'''
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)
        
        if artists is not None:
            self.set_artists(artists)

    def __eq__(self, other) -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Track): object to compare to

        Returns:
            bool: whether or not the objects are considered equal
        """

        if self.get_id() != other.get_id():
            return False
        if self.name != other.name:
            return False
        
        # Check if each artist exists
        if len(self.get_artists()) != len(other.get_artists()):
            return False
        for artist in self.get_artists():
            found = False
            current_id = artist.get_id()
            other_artists = other.get_artists()
            for other_artist in other_artists:
                if current_id == other_artist.get_id():
                    found = True
                    break
            if not found:
                return False
        return True

    # ---- Getter Functions ----

    def get_artists(self) -> list[artist.Artist]:
        """Returns list of artists accociated with this track.

        Returns:
            list[artist.Artist]: list of the contained artists
        """
        return self.artists

    # ---- Setter Functions ----
   
    def set_artists(self, artists: list):
        '''Takes a list of artists and sets them for the track object'''
        self.artists = []
        for artist in artists:
            self.artists.append(artist)

    # ---- Other Functions ----