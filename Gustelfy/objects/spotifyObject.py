# external
# python native
import logging
import time
from abc import ABC, abstractmethod
# project

class SpotifyObject(ABC):
    """Base class for all spotify objects.
    """
    id: str
    name: str
    timestamp: int
    expires_after = 60*60*4 # time in seconds

    @abstractmethod
    def __init__():
        pass

    def __eq__(self, other):
        return self.is_equal(other)

    def __str__(self):
        if self.name is None:
            return "None"
        else:
            return self.name

    def __repr__(self):
        return self.__str__()

    # ---- Getter Functions ----

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_timestamp(self) -> int:
        return self.timestamp

    def is_expired(self) -> bool:
        if int(time.time()) - self.timestamp > self.expires_after:
            return True
        else:
            return False

    # ---- Setter Functions ----

    def set_id(self, id: str):
        if id is None:
            raise TypeError("None not allowed")
        else:
            self.id = id

    def set_name(self, name: str):
        if name is None:
            raise TypeError    
        else:
            self.name = name

    def set_timestamp(self, timestamp=int(time.time())):
        self.timestamp = timestamp

    def set_expires_after(self, seconds):
        self.expires_after = seconds
    
    # ---- Other Functions ----

    @abstractmethod
    def is_equal(self, other):
        pass    

    @abstractmethod
    def merge(self, other):
        """Combine information of two different Spotify objects into one.
        Most recent timestamp wins.

        Args:
            other (spotifyObject): object to merge with
        """
        