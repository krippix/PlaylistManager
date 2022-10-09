class Playlist:
    
    id: str
    name: str
    owner_id: str
    is_managed: bool
    
    def __init__(self, id=str, name=str, owner_id=str):
        self.set_id(id)
        self.set_name(name)
        self.set_owner_id(owner_id)

    def __str__(self):
        return self.get_name()
    def __repr__(self):
        return self.__str__()

    ########
    # getter

    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def is_managed(self) -> bool:
        return self.is_managed
    
    #########
    # setter
    
    def set_id(self, id: str):
        '''Sets the playlists spotify id'''
        self.id = id

    def set_name(self, name: str):
        '''Sets the playlists name'''
        self.name = name

    def set_owner_id(self, id: str):
        '''Sets the playlist owners id'''
        self.owner_id = id

    def set_managed(self, is_managed: bool):
        self.is_managed = is_managed