# external
# python native
import time
import logging
# project
from objects import spotifyObject
from objects import track, artist

class Album(spotifyObject.SpotifyObject):
    """Spotify Album object, contains tracks.
    """

    artists: list[artist.Artist]
    tracks: list[track.Track]
    images: list[dict]
    release_date: str
    total_tracks: int
    popularity: int

    def __init__(self,
                id: str,
                name=None,
                artists=[],
                tracks=[],
                images=[],
                release_date=None,
                total_tracks=None,
                timestamp=int(time.time()),
                popularity=None
                ):
        """
        Creates Spotify Album Object

        Args:
            - id           : (str) Spotify Album ID 
            - name         : (str) Album Name
            - timestamp    : (int) timestamp -> defaults to current time
            - artists      : (list[Artist]) List of Album artists
            - tracks       : (list[Track]) List of Album tracks
            - images       : (list[{"width": w, "url" : u, "height" : h}]) List of image dicts
            - release_date : (str) release date string
            - total_tracks : (int) total tracks in album, may not match with len(tracks)
            - popularity   : (int) popularity 0-100
        """
        self.logger = logging.getLogger(__name__)
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)

        self.set_artists(artists)
        self.set_tracks(tracks)
        self.set_images(images)
        self.set_release_date(release_date)
        self.set_total_tracks(total_tracks)
        self.set_popularity(popularity)

    # ---- Getter Functions ----

    def get_artists(self) -> list[artist.Artist]:
        return self.artists

    def get_tracks(self) -> list[track.Track]:
        return self.tracks

    def get_images(self) -> list[dict]:
        return self.images
    
    def get_image_url(self) -> str:
        """Returns first found image url

        Returns:
            str: image url
        """
        try:
            return self.images[0]["url"]
        except IndexError:
            return ""

    def get_release_date(self) -> str:
        return self.release_date

    def get_total_tracks(self) -> int:
        return self.total_tracks

    def get_popularity(self) -> int:
        return self.popularity

    # ---- Setter Functions ----

    def set_name(self, name: str):
        self.name = name
    
    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks

    def set_artists(self, artists: list[artist.Artist]):
        self.artists = artists

    def set_images(self, images):
        """Set list of image tuples

        Args:
            images (list[tuple(int,str,int)]): (height,url,width)
        """
        self.images = images

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
        if len(self.get_tracks()) != len(other.get_tracks()):
            return False
        if len(self.get_artists()) != len(other.get_artists()):
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
    
    def merge(self, other: 'Album') -> 'Album':
        """Merges other Album object into this one

        Args:
            other (Album): Album to merge into this object

        Returns:
            self: _description_
        """
        # Check if wrong input
        if not isinstance(other, Album):
            raise TypeError()
        if self.get_id() != other.get_id():
            self.logger.error("Cannot merge different Album objects.")
            return
        # Decide who is newer
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
        # artists
        artist_overlap = [n_art.merge(o_art) for n_art in new.get_artists() for o_art in old.get_artists() if o_art.get_id() == n_art.get_id()]
        for n_art in new.get_artists():
            match = False
            for art in artist_overlap:
                if n_art.get_id() == art.get_id():
                    match = True
            if not match:
                artist_overlap.append(n_art)
        self.set_artists(artist_overlap)
        # tracks
        track_overlap = [n_track.merge(o_track) for n_track in new.get_tracks() for o_track in old.get_tracks() if o_track.get_id() == n_track.get_id()]
        for n_track in new.get_tracks():
            match = False
            for trk in track_overlap:
                if n_track.get_id() == trk.get_id():
                    match = True
            if not match:
                track_overlap.append(n_track)
        self.set_tracks(track_overlap)
        # images
        if len(new.get_images()) == 0:
            self.set_tracks(old.get_images())
        else:
            self.set_tracks(new.get_images())
        # release_date
        if new.get_release_date() is None:
            self.set_release_date(old.get_release_date())
        else:
            self.set_release_date(new.get_release_date())
        # total_tracks
        if new.get_total_tracks() is None:
            self.set_total_tracks(old.get_total_tracks())
        else:
            self.set_total_tracks(new.get_total_tracks())
        # popularity
        if new.get_popularity() is None:
            self.set_popularity(old.get_popularity())
        else:
            self.set_popularity(new.get_popularity())
        return self