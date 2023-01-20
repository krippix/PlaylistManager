# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import track, artist

class Album(spotifyObject.SpotifyObject):
    """Spotify Album object, contains tracks.
    """

    artists: list[artist.Artist]
    tracks: list[track.Track]

    def __init__(self, id: str, name: str, tracks: list[track.Track], artists: list[artist.Artist], timestamp=int(time.time())):
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_artists(artists)
        self.set_tracks(tracks)

    # ---- Getter Functions ----

    def get_artists() -> list[artist.Artist]:
        return self.artists

    def get_tracks() -> list[track.Track]:
        return self.tracks

    # ---- Setter Functions ----
    
    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks

    def set_artists(self, artists: list[artist.Artist]):
        self.aritsts = artists

    # ---- Other Functions ----

    def is_equal(self, other: 'Album') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (album.Album): album to compare to

        Returns:
            bool: whether or not they are equal
        """
        if other.get_id() != self.get_id():
            return False
        if other.get_name() != self.get_name():
            return False
        
        # Compare amount of tracks and artists
        if len(self.get_tracks) != len(other.get_tracks()):
            return False
        if len(self.get_artists) != len(other.get_artists()):
            return False

        # Check if artists are equal
        for artist in self.get_artists():
            subresult = False
            for other_artist in other.get_artists():
                if other_artist == artist:
                    subresult = True
            if not subresult:
                return False
        
        # Check if tracks are equal
        for track in self.get_tracks():
            subresult = False
            for other_track in other.get_tracks():
                if other_track == track:
                    subresult = True
            if not subresult:
                return False
        return True