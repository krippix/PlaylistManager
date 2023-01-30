# external
# python native
import time
# project
from Gustelfy.objects import spotifyObject
from Gustelfy.objects import artist, album


class Track(spotifyObject.SpotifyObject):
    """Spotify Track object, contains track (song) information
    """

    artists = []
    duration_ms: int
    album: 'album.Album'
    disc_number: int
    track_number: int
    explicit: bool
    popularity: int
    
    def __init__(self,
                id: str,
                name: str,
                artists: list[artist.Artist],
                timestamp=int(time.time()),
                duration_ms=None,
                album=None,
                disc_number=None,
                track_number=None,
                explicit=None,
                popularity=None,
                ):
        self.set_id(id)
        self.set_name(name)
        self.set_timestamp(timestamp)
        self.set_artists(artists)
        self.set_duration_ms(duration_ms)
        self.set_album(album)
        self.set_disc_number(disc_number)
        self.set_track_number(track_number)
        self.set_explicit(explicit)
        self.set_popularity(popularity)        

    # ---- Getter Functions ----

    def get_artists(self) -> list[artist.Artist]:
        """Returns list of artists accociated with this track.

        Returns:
            list[artist.Artist]: list of the contained artists
        """
        return self.artists

    def get_duration_ms(self) -> int:
        """Returns track's duration in ms

        Returns:
            int: duration in ms
        """
        return self.duration_ms

    def get_album(self) -> 'album.Album':
        return self.album

    def get_disc_number(self) -> int:
        return self.disc_number

    def get_track_number(self) -> int:
        return self.track_number

    def is_explicit(self) -> int:
        """Returns bool value of explicity as int 1 or 0

        Returns:
            bool:
        """
        return self.explicit
    
    def get_popularity(self) -> int:
        return self.popularity

    # ---- Setter Functions ----
   
    def set_artists(self, artists: list):
        '''Takes a list of artists and sets them for the track object'''
        self.artists = []
        for artist in artists:
            self.artists.append(artist)

    def set_duration_ms(self, duration: int):
        """Sets track's duration in ms

        Args:
            duration (int): duration in ms
        """
        self.duration_ms = duration

    def set_album(self, album: 'album.Album'):
        self.album = album

    def set_disc_number(self, number: int):
        self.disc_number = number

    def set_track_number(self, track_number: int):
        self.track_number = track_number

    def set_explicit(self, explicit: bool):
        self.explicit = explicit

    def set_popularity(self, popularity: int):
        self.popularity = popularity

    # ---- Other Functions ----

    def is_equal(self, other: 'Track') -> bool:
        """Defines behaviour of the '==' operator

        Args:
            other (Track): object to compare to

        Returns:
            bool: whether or not the objects are considered equal
        """
        if other is None or not isinstance(other, Track):
            return False
        if self.get_id() != other.get_id():
            return False
        if self.name != other.name:
            return False
        
        # Check if each artist exists
        if len(self.get_artists()) != len(other.get_artists()):
            return False
        for artist in self.get_artists():
            found = False
            current_id = artist.get_id()
            other_artists = other.get_artists()
            for other_artist in other_artists:
                if current_id == other_artist.get_id():
                    found = True
                    break
            if not found:
                return False
        return True

    def merge(self, other: 'Track'):
        """Merges two track objects to their newest state, takes information out of both for any None values

        Args:
            other (Track): Track to merge with

        Raises:
            TypeError: No Track object provided

        Returns:
            Track: merged track object
        """
        # Check wrong input 
        if not isinstance(other, Track):
            raise TypeError()
        if self.get_id() != other.get_id() or other is None:
            self.logger.error("Cannot merge different Track objects.")
            return
        # Check who is "newer"
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
        self.timestamp = new.get_timestamp()
        # artists
        # merge artists that are in both objects
        artist_list = [n_art.merge(o_art) for n_art in new.get_artists() for o_art in old.get_artists() if n_art.get_id() == o_art.get_id()]
        # add artists that only exist in the new object
        for n_art in new.get_artists():
            match = False
            for art in artist_list:
                if n_art.get_id() == art.get_id():
                    match = True
                    break
            if not match:
                artist_list.append(n_art)
        self.set_artists(artist_list)
        # duration
        if new.get_duration_ms() is None and old.get_duration_ms() is not None:
            self.set_duration_ms(old.get_duration_ms())
        else:
            self.set_duration_ms(new.get_duration_ms())
        # album
        if new.get_album() is None:
            self.set_album(old.get_album())
        else:
            self.set_album(new.get_album().merge(old.get_album()))
        # disc_number
        if new.get_disc_number() is None:
            self.set_disc_number(old.get_disc_number())
        else:
            self.set_album(new.disc_number())
        # track_number
        if new.get_track_number() is None:
            self.set_track_number(old.get_track_number())
        else:
            self.set_track_number(new.get_track_number())
        # explicit
        if new.is_explicit() is None:
            self.set_explicit(old.is_explicit())
        else:
            self.set_explicit(new.is_explicit())
        # popularity
        if new.get_popularity() is None:
            self.set_popularity(old.get_popularity())
        else:
            self.set_popularity(new.get_popularity())
        return self