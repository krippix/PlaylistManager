import objects.artist

class Track:

    id: str
    name: str
    artist = []
    
    def __init__(self, id: str, name: str, artists: list):
        '''Creates new artist object with the provided data'''
        self.set_id(id)
        self.set_name(name)
        
        if artists is not None:
            self.set_artists(artists)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

    ########
    # getter

    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.id

    def get_artists(self) -> list:
        '''Returns list containing artist objects'''
    
    
    #########
    # setter
    
    def set_id(self, id: str):
        '''Sets the tracks spotify id'''
        self.id = id

    def set_name(self, name: str):
        '''Sets the tracks name'''
        self.name = name
   
    def set_artists(self, artists: list):
        '''Takes a list of artists and adds them to the track'''
        for artist in artists:
            self.artist.append(artist)
        