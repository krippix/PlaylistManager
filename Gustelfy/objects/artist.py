# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject

class Artist(spotifyObject.SpotifyObject):
    """Spotify Artist object. Contains genres.
    """
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
    
    def get_image_url(self) -> str:
        """Returns first found image url

        Returns:
            str: image url
        """
        try:
            return self.images[0][1]
        except Exception:
            return "https://t.scdn.co/images/3099b3803ad9496896c43f22fe9be8c4.png"

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
        # images
        if len(new.get_images()) != 0:
            self.set_images(new.get_images())
        else:
            self.set_images(old.get_images())
        # popularity
        if new.get_popularity() is None:
            self.set_popularity(old.get_popularity())
        else:
            self.set_popularity(new.get_popularity())
        # followers
        if new.get_followers() is None:
            self.set_popularity(old.get_popularity())
        else:
            self.set_popularity(new.get_popularity())
        return self