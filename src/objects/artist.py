class Artist:

    id: str
    name: str
    timestamp: int
    
    def __init__(self, id, name):
        '''Creates new artist object with the provided data'''
        self.id = id
        self.name = name

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

    ########
    # setter

    def set_id(self, id: str):
        '''Sets the playlists spotify id'''
        self.id = id

    def set_name(self, name: str):
        '''Sets the playlists name'''
        self.name = name