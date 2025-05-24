# external
# python native
import time
# project
import util.config
import objects.track, objects.artist, objects.playlist


import objects.artist

class Track:

    id: str
    name: str
    artists = []
    timestamp: int
    expires_after: int
    
    def __init__(self, id: str, name: str, artists: list, timestamp: int):
        '''Creates new artist object with the provided data'''
        self.set_id(id)
        self.set_name(name)
        self.timestamp = timestamp
        
        if artists is not None:
            self.set_artists(artists)

    def __str__(self):
        '''Defines behaviour within print statements.'''
        return self.name

    def __repr__(self):
        '''Defines behaviour if eg. withn a list in a print statement: [object,]'''
        return self.__str__()

    def __eq__(self, other):
        '''Defines behaviour of == operator'''

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


    ########
    # getter

    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.name

    def get_artists(self) -> list[objects.artist.Artist]:
        '''Returns list containing artist objects'''
        return self.artists

    def get_timestamp(self) -> int:
        return self.timestamp

    def is_expired(self) -> bool:
        ''''''
        if int(time.time()) - self.timestamp > util.config.Config().get_config(category="EXPIRY",key="tracks"):
            return True
        else:
            return False
    
    #########
    # setter
    
    def set_id(self, id: str):
        '''Sets the tracks spotify id'''
        self.id = id

    def set_name(self, name: str):
        '''Sets the tracks name'''
        self.name = name
   
    def set_artists(self, artists: list):
        '''Takes a list of artists and sets them for the track object'''
        self.artists = []
        for artist in artists:
            self.artists.append(artist)
        