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
    image_url: str
    
    def __init__(self,
                id: str,
                name: str,
                genres=[],
                timestamp=int(time.time()),
                image_url="https://i.scdn.co/image/ab6775700000ee8555c25988a6ac314394d3fbf5"
                ):
        """Initialises new Artist object

        Args:
            id (str): _description_
            name (str): _description_
            genres (list, optional): _description_. Defaults to [].
            timestamp (_type_, optional): _description_. Defaults to int(time.time()).
            image_url (str, optional): _description_. Defaults to Spotify Logo
        """
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_genres(genres)
        self.set_image_url(image_url)

    # ---- Getter Functions ----

    def get_genres(self) -> list[str]:
        return self.genres

    def get_image_url(self) -> str:
        return self.image_url

    # ---- Setter Functions ----

    def set_genres(self, genres: list[str]):
        self.genres = genres

    def set_image_url(self, url: str):
        self.image_url = url

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