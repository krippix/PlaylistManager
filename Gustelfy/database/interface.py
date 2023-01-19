# external
# python native
import logging
from abc import ABC, abstractmethod
# project
from Gustelfy.objects import *
from Gustelfy.util import config


class Interface(ABC):
    '''
    Base class for all Database connections.
    This class is not supposed to check if for example a song already exists!
    '''

    def __init__(self):
        '''Connect to the database.'''
        self.settings = config.Config()
        self.connect_database()

    # ---- Getter Functions ----

    @abstractmethod
    def get_album(self, id: str) -> album.Album | None:
        '''Returns album with given id.'''

    @abstractmethod
    def get_artist(self, id: str) -> artist.Artist | None:
        '''Returns artist object or None if nothing was found.'''

    @abstractmethod
    def get_favorites(self, user_id: str) -> list[track.Track]:
        '''Returns list of songs withing the user'''

    @abstractmethod
    def get_genres(self, artist_id: str) -> list[str]:
        '''Returns list of genres associated with the given artist'''

    @abstractmethod
    def get_playlist(self, id: str) -> playlist.Playlist | None:
        '''Returns playlist object or None if nothing was found.'''    

    @abstractmethod
    def get_track(self, id: str) -> track.Track | None:
        '''Returns track object. Or None, if nothing was found.'''

    @abstractmethod
    def get_user(self, id: str) -> user.User | None:
        '''Returns user object with given id.'''

    # ---- Setter Functions ----

    # ---- Other Functions ----
    
    @abstractmethod
    def connect_database(self):
        '''Establishes connection to database'''

    # -- add --
    
    @abstractmethod
    def add_album(self, album: album.Album):
        '''Adds an album to the database. Overwrites if already present.'''

    @abstractmethod
    def add_artist(self, artist: artist.Artist):
        '''Adds an artist to the database. Overwrites if already present.'''

    @abstractmethod
    def add_favorite(self, user: user.User, track: track.Track):
        '''Adds a favorite to the database. Overwrites if already present.'''

    @abstractmethod
    def add_genre(self, genre: str):
        '''Adds a genre to the database. Overwrites if already present.'''

    @abstractmethod
    def add_playlist(self, playlist: playlist.Playlist):
        '''Adds a playlist to the database. Overwrites if already present.'''    

    @abstractmethod
    def add_track(self, track: track.Track):
        '''Adds a track to the database. Overwrites if already present.'''

    @abstractmethod
    def add_user(self, user: user.User):
        '''Adds a user to the database. Overwrites if already present.'''

    # -- Update --
    @abstractmethod
    def update_favorites(self, delta: tuple[list[track.Track], list[track.Track]]):
        """Updates list of favorites with given input

        Args:
            delta (tuple[list[track.Track], list[track.Track]]): 0 - added tracks; 1 - removed tracks
        """

    # ---- Database integrity ----

    @abstractmethod
    def check(self):
        '''Checks if the database contains all required tables. Attempts to fix any problems.'''
    
    @abstractmethod
    def create_database(self):
        '''Creates Database structure.'''

    @abstractmethod
    def table_exists(self, table: str) -> bool:
        '''Checks if provided table exists.'''