# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject

class Artist(spotifyObject.SpotifyObject):
    """Spotify Artist object. Contains genres.
    """
    genres: list[str]
    images: list[dict]
    popularity: int
    followers: int
    
    def __init__(self,
                id: str,
                name: str,
                genres=[],
                timestamp=int(time.time())
                ):
        """Creates Spotify Artist object

        Args:
            id: _description_
            name: _description_
            timestamp: _description_. Defaults to int(time.time()).
            genres: _description_. Defaults to [].
        """
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_genres(genres)

    def as_dict(self) -> dict:
        """Returns self as dict
        """
        as_dict = {
            "id"        : self.id,
            "name"      : self.name,
            "genres"    : str(self.genres),
            "timestamp" : str(self.timestamp)
        }
        return as_dict

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
        if other is None:
            return False
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
    
    def merge(self, other: 'Artist'):
        """Merges another artist object into this one. None attributes are handled.
        Information is pulled from more recent timestamp

        Args:
            other (Artist): Object to merge into this one
        """
        # Check for wrong input
        if not isinstance(other, Artist):
            raise TypeError()
        if self.get_id() != other.get_id() or other is None:
            self.logger.error("Cannot merge different Artist objects")
            return
        # Determine newer object
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
        self.set_timestamp(new.get_timestamp())
        # genres (cannot be None)
        genres = [n_genre for n_genre in new.get_genres() for o_genre in old.get_genres() if n_genre == o_genre] # overlap
        for n_genre in new.get_genres():
            if n_genre not in genres:
                genres.append(n_genre)
        self.set_genres(genres)

        return self