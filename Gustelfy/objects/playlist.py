# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import track

class Playlist(spotifyObject.SpotifyObject):
    
    managed: bool
    tracks = []
    genres: list[str]
    
    def __init__(self, 
                id: str, 
                name: str,
                tracks    = [],
                managed   = False,
                timestamp = int(time.time()),
                genres    = []
                ):
        """Creates a Spotify Playlist object

        Args:
            - id (str): Spotify ID
            - name (str): Name
            - tracks (list, optional): Playlist tracks. Defaults to [].
            - managed (int, optional): Managed flag (for this software)
            - timestamp (int, optional): Defaults to int(time.time()).
            - genres (list, optional): Genres (For management).
        """
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)
        self.set_tracks(tracks)
        self.set_managed(managed)
        self.set_genres(genres)

    def as_dict(self) -> dict:
        """Returns self as dict
        """
        tracks = [x.as_dict() for x in self.tracks]
        as_dict = {
            "id"        : self.id,
            "name"      : self.name,
            "genres"    : str(self.genres),
            "timestamp" : str(self.timestamp),
            "tracks"    : tracks
        }
        return as_dict

    # ---- Getter Functions ----

    def is_managed(self) -> bool:
        return self.managed

    def get_tracks(self) -> list[track.Track]:
        return self.tracks

    def get_genres(self) -> list[str]:
        return self.genres

    # ---- Setter Functions ----

    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks

    def set_managed(self, is_managed: bool):
        self.managed = is_managed

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
        if other is None or not isinstance(other, Playlist):
            return False
        if self.get_id() != other.get_id():
            return False
        if self.get_name() != other.get_name():
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
        # genres
        if len(new.get_genres()) == 0:
            self.set_genres(old.get_genres())
        else:
            self.set_genres(new.get_genres())
        return self