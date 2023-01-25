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
    images: list[tuple()]
    release_date: str
    total_tracks: int
    popularity: int

    def __init__(self,
                id: str,
                name: str,
                artists: list[artist.Artist],
                tracks=[],
                images=[],
                release_date=None,
                total_tracks=None,
                timestamp=int(time.time()),
                popularity=None
                ):
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_artists(artists)
        self.set_tracks(tracks)
        self.set_images(images)
        self.set_release_date(release_date)
        self.set_total_tracks(total_tracks)

    # ---- Getter Functions ----

    def get_artists(self) -> list[artist.Artist]:
        return self.artists

    def get_tracks(self) -> list[track.Track]:
        return self.tracks

    def get_images(self) -> str:
        return self.images

    def get_release_date(self) -> str:
        return self.release_date

    def get_total_tracks(self) -> int:
        return self.total_tracks

    def get_popularity(self) -> int:
        return self.popularity

    # ---- Setter Functions ----
    
    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks

    def set_artists(self, artists: list[artist.Artist]):
        self.aritsts = artists

    def set_images(self, images):
        """Set list of image tuples

        Args:
            images (list[tuple(int,str,int)]): (height,url,width)
        """
        self.image_url = images

    def set_release_date(self, date: str):
        self.release_date = date

    def set_total_tracks(self, total_tracks: int):
        self.total_tracks = total_tracks

    def set_popularity(self, popularity: int):
        self.popularity = popularity

    # ---- Other Functions ----

    def is_equal(self, other: 'Album') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (album.Album): album to compare to

        Returns:
            bool: whether or not they are equal
        """
        if other is None:
            return False
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