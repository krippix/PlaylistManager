# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject

class Artist(spotifyObject.SpotifyObject):
    """Spotify Artist object. Contains genres.
    """

    name: str
    genres: list[str]
    
    def __init__(self, id: str, name: str, genres=[], timestamp=int(time.time())):
        '''Creates new artist object with the provided data'''
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_genres(genres)

    # ---- Getter Functions ----

    def get_genres(self) -> list[str]:
        return self.genres

    # ---- Setter Functions ----

    def set_genres(self, genres: list[str]):
        self.genres = genres

    # ---- Other Functions ----

    def is_equal(self, other: 'Artist') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Artist): artist beeing compared

        Returns:
            bool: whether or not they are equal
        """
        if self.get_id() != other.get_id():
            return False
        if self.get_name() != other.get_name():
            return False

        # Check if genres match up
        if len(self.get_genres()) != len(other.get_genres()):
            return False

        for genre in self.get_genres():
            subresult = False
            for other_genre in other.get_gernes():
                if genre == other_genre:
                    subresult = True
            if not subresult:
                return False
        return True