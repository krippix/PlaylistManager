# external
# python native
import time
# project
from Gustelfy.util import config
from Gustelfy.objects import track

class Album():
    '''Represents a spotify Album'''
    id: str
    name: str
    timestamp: int
    tracks: list[track.Track]

    def __init__(self, id: str, name: str, timestamp=0, **kwargs):
        '''If no timestamp is provided, current time will be set.'''
        self.id = id
        self.name = name
        if timestamp == 0:
            self.timestamp == int(time.time())

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
        if int(time.time()) - self.timestamp > int(config.Config().get_config(category="EXPIRY",key="album")):
            return True
        else:
            return False

    # ---- Setter Functions ----
    
    def set_id(self, id: str):
        self.id = id

    def set_name(self, name: str):
        self.name = name

    def set_tracks(self, tracks: list[track.Track]):
        self.tracks = tracks