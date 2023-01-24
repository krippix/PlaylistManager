# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import artist


class Track(spotifyObject.SpotifyObject):
    """Spotify Track object, contains track (song) information
    """

    artists = []
    duration: int
    disc_number: int
    explicit: bool
    
    def __init__(self,
                id: str,
                name: str,
                artists=list[artist.Artist],
                timestamp=int(time.time()),
                duration_ms=0,
                disc_number=1,
                explicit=0
                ):
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)
        self.set_artists(artists)
        self.set_duration(duration_ms)
        self.set_disc_number(disc_number)
        self.set_explicit(explicit)        

    # ---- Getter Functions ----

    def get_artists(self) -> list[artist.Artist]:
        """Returns list of artists accociated with this track.

        Returns:
            list[artist.Artist]: list of the contained artists
        """
        return self.artists

    def get_duration(self) -> int:
        """Returns track's duration in ms

        Returns:
            int: duration in ms
        """
        return self.duration

    def get_disc_number(self) -> int:
        return self.disc_number

    def is_explicit(self) -> int:
        """Returns bool value of explicity as int 1 or 0

        Returns:
            int: 0 || 1
        """
        if self.explicit:
            return 1
        else:
            return 0

    # ---- Setter Functions ----
   
    def set_artists(self, artists: list):
        '''Takes a list of artists and sets them for the track object'''
        self.artists = []
        for artist in artists:
            self.artists.append(artist)

    def set_duration(self, duration: int):
        """Sets track's duration in ms

        Args:
            duration (int): duration in ms
        """
        self.duration = duration

    def set_disc_number(self, number: int):
        self.disc_number = number

    def set_explicit(self, explicit: bool):
        self.explicit = explicit

    # ---- Other Functions ----

    def is_equal(self, other) -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Track): object to compare to

        Returns:
            bool: whether or not the objects are considered equal
        """
        if other is None:
            return False
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