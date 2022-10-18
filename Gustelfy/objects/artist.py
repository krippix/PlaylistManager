# external
# python native
import time
# project
import util.config

class Artist:

    id: str
    name: str
    timestamp: int
    genres: list
    
    def __init__(self, id: str, name: str, timestamp: int, **kwargs):
        '''Creates new artist object with the provided data'''
        self.id = id
        self.name = name
        self.timestamp = timestamp
        self.genres = kwargs.get('genres', [])

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()        

    ########
    # getter

    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.name

    def get_genres(self) -> list:
        return self.genres

    def is_expired(self) -> bool:
        ''''''
        if int(time.time()) - self.timestamp > int(util.config.Config().get_config(category="EXPIRY",key="artists")):
            return True
        else:
            return False

    ########
    # setter

    def set_id(self, id: str):
        '''Sets the playlists spotify id'''
        self.id = id

    def set_name(self, name: str):
        '''Sets the playlists name'''
        self.name = name

    def set_genres(self, genres: list):
        self.genres = genres