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
    
    def __init__(self, id: str, name: str, owner_id: str, tracks=[], managed=False, timestamp=int(time.time())):
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_owner_id(owner_id)
        self.set_tracks(tracks)
        self.set_managed(managed)

    # ---- Getter Functions ----

    def get_owner_id() -> str:
        return self.owner_id

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

    # ---- Setter Functions ----

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

    # ---- Other Functions ----

    def is_equal(self, other: 'Playlist') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Playlist): playlist to compare to

        Returns:
            bool: whether or not they are equal
        """
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
