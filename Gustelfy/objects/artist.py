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
    images: list[tuple()]
    popularity: int
    followers: int
    
    def __init__(self,
                id: str,
                name: str,
                genres=[],
                timestamp=int(time.time()),
                images=[],
                popularity=None,
                followers=None
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
        self.set_images(images)
        self.set_popularity(popularity)
        self.set_followers(followers)

    # ---- Getter Functions ----

    def get_genres(self) -> list[str]:
        return self.genres

    def get_images(self) -> list[tuple()]:
        return self.images

    def get_popularity(self) -> int:
        return self.popularity

    def get_followers(self) -> int:
        return self.followers

    # ---- Setter Functions ----

    def set_genres(self, genres: list[str]):
        self.genres = genres

    def set_images(self, images: list[tuple()]):
        self.images = images

    def set_popularity(self, popularity: int):
        self.popularity = popularity
    
    def set_followers(self, followers: int):
        self.followers = followers

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