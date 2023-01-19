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

    @abstractmethod
    def __eq__():
        pass

    def __str__(self):
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
        self.id = id

    def set_name(self, name: str):
        self.name = name

    def set_timestamp(self, timestamp=int(time.time())):
        self.timestamp = timestamp

    def set_expires_after(seconds):
        self.expires_after = seconds
    
    # ---- Other Functions ----