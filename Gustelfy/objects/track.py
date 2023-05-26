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
    
    def __init__(self,
                id: str,
                name: str,
                artists: list[artist.Artist],
                timestamp=int(time.time())
                ):
        """Creates Spotify track object

        Args:
            id: _description_
            name: _description_
            artists: _description_
            timestamp: _description_. Defaults to int(time.time()).
        """
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)
        self.set_artists(artists)  

    def as_dict(self) -> dict:
        """Returns self as dict
        """
        dict_artists = [x.as_dict() for x in self.artists]

        dict_obj = {
            "id"      : self.id,
            "name"    : self.name,
            "artists" : dict_artists
        }
        return dict_obj

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
        if artists is None:
            raise TypeError
        else:
            self.artists = artists

    # ---- Other Functions ----

    def is_equal(self, other: 'Track') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Track): object to compare to

        Returns:
            bool: whether or not the objects are considered equal
        """
        if other is None or not isinstance(other, Track):
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

    def merge(self, other: 'Track'):
        """Merges two track objects to their newest state, takes information out of both for any None values

        Args:
            other (Track): Track to merge with

        Raises:
            TypeError: No Track object provided

        Returns:
            Track: merged track object
        """
        # Check wrong input 
        if not isinstance(other, Track):
            raise TypeError()
        if self.get_id() != other.get_id() or other is None:
            self.logger.error("Cannot merge different Track objects.")
            return
        # Check who is "newer"
        if self.get_timestamp() < other.get_timestamp():
            new = other
            old = self
        else:
            new = self
            old = other
        # name
        if new.get_name() != old.get_name():
            self.set_name(new.get_name())
        # timestamp
        self.timestamp = new.get_timestamp()
        # artists
        # merge artists that are in both objects
        artist_list = [n_art.merge(o_art) for n_art in new.get_artists() for o_art in old.get_artists() if n_art.get_id() == o_art.get_id()]
        # add artists that only exist in the new object
        for n_art in new.get_artists():
            match = False
            for art in artist_list:
                if n_art.get_id() == art.get_id():
                    match = True
                    break
            if not match:
                artist_list.append(n_art)
        self.set_artists(artist_list)
        return self