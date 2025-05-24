# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import track

class Playlist(spotifyObject.SpotifyObject):
    
    owner_id: str
    managed: bool
    tracks = []
    description: str
    image_url: str
    genres: list[str]
    
    def __init__(self, 
                id: str, 
                name: str,
                owner_id: str,
                tracks=[],
                managed=0,
                timestamp=int(time.time()),
                user_id=None,
                description=None,
                image_url=None,
                genres=[]
                ):
        """Creates a Spotify Playlist object

        Args:
            id (str): Spotify ID of the Playlist
            name (str): Playlist (display) name
            user_id (str): Spotify ID of the user following the playlist in this context
            owner_id (str): Spotify ID of the Playlist owner
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
        self.set_owner_id(owner_id)
        self.set_tracks(tracks)
        self.set_managed(managed)
        self.set_description(description)
        self.set_image_url(image_url)
        self.set_genres(genres)

    # ---- Getter Functions ----

    def get_user_id(self) -> str:
        return self.user_id

    def get_owner_id(self) -> str:
        return self.owner_id

    def is_managed(self) -> bool:
        if self.managed:
            return 1
        else:
            return 0

    def get_tracks(self) -> list[track.Track]:
        return self.tracks

    def get_description(self) -> str:
        return self.description

    def get_image_url(self) -> str:
        return self.image_url

    def get_genres(self) -> list[str]:
        return self.genres

    # ---- Setter Functions ----

    def set_user_id(self, user_id: str):
        self.user_id = user_id

    def set_owner_id(self, owner_id: str):
        self.owner_id = owner_id

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
        if self.get_owner_id() != other.get_owner_id():
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

    def merge(self, other: 'Playlist') -> 'Playlist':
        """Merges another Playlist object into this one. Most recent timestamp "wins" conflicts

        Args:
            other (Playlist): Playlist to merge into this object

        Returns:
            Playlist: returns self after merge
        """
        # Check for wrong input
        if not isinstance(other, Playlist):
            raise TypeError()
        if self.get_id() != other.get_id():
            self.logger.error("Connot merge different Playlist objects.")
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
        # owner_id
        if new.get_owner_id() != old.get_owner_id():
            self.set_owner_id(new.get_owner_id())
        # managed
        if new.is_managed() is None:
            self.set_managed(old.is_managed())
        else:
            self.set_managed(new.is_managed())
        # tracks
        tracks = [n_trk.merge(o_trk) for n_trk in new.get_tracks() for o_trk in old.get_tracks if o_trk.get_id() == n_trk.get_id()]
        for n_trk in new.get_tracks():
            match = False
            for trk in tracks:
                if n_trk.get_id() == trk.get_id():
                    match = True
            if not match:
                tracks.append(n_trk)
        self.set_tracks(tracks)
        # description
        if new.get_description() is None:
            self.set_description(old.get_description())
        else:
            self.set_description(new.get_description())
        # image_url
        if new.get_image_url() is None:
            self.set_image_url(old.get_image_url())
        else:
            self.set_image_url(new.set_image_url())
        # genres
        if len(new.get_genres()) == 0:
            self.set_genres(old.get_genres())
        else:
            self.set_genres(new.get_genres())
        return self