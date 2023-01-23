# external
# python native
import time
# project


class User(spotifyObject.SpotifyObject):
    """Spotify user object
    """
    id: str
    display_name: str
    email: str
    expires_at: int
    api_token: str
    image_url: str
    timestamp: int
    
    def __init__(self, id: str, display_name="UNKNOWN",email="noreply@spotify.com",expires_at=0,api_token="?",image_url="https://spotify.com/yeet.png", timestamp=int(time.time())):
        self.id = id
    
    # ---- Getter Functions ----

    def get_id(self) -> str:
        return self.id

    def get_display_name(self) -> str:
        return self.display_name

    def get_email(self) -> str:
        return self.email

    def get_expires_at(self) -> int:
        return self.expires_at

    def get_api_token(self) -> str:
        return self.api_token

    def get_image_url(self) -> str:
        return self.image_url

    def get_timestamp(self) -> int:
        return self.timestamp

    # ---- Setter Functions ----

    def set_id(self, id: str):
        self.id = id 
    
    def set_display_name(self, name: str):
        self.name = name

    def set_email(self, email: str):
        self.email = email

    def set_expires_at(self, expires_at: int):
        self.expires_at = expires_at

    def set_api_token(self, api_token: str):
        self.api_token = api_token

    def set_image_url(self, url: str):
        self.image_url = url

    def set_timestamp(self, timestamp: int):
        self.timestamp = timestamp

    # ---- Other Functions ----