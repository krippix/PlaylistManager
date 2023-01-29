# external
# python native
import time
import logging
# project


class User():
    """Spotify user object
    """
    id: str
    display_name: str
    image_url: str
    followers: int
    timestamp: int
    # Auth stuff api
    token: dict

    def __init__(self, 
                id: str,
                display_name=None,
                image_url=None,
                followers=None,
                timestamp=int(time.time()),
                # API
                token=None
                ):
        """Spotify user, may include authentication data.

        Args:
            id (str): _description_
            display_name (_type_, optional): _description_. Defaults to None.
            image_url (_type_, optional): _description_. Defaults to None.
            followers (_type_, optional): _description_. Defaults to None.
            timestamp (_type_, optional): _description_. Defaults to int(time.time()).
            access_token (dict, optional): Contains user access token. Defaults to None.

        """
        self.logger = logging.getLogger(__name__)
        self.set_id(id)
        self.set_display_name(display_name)
        self.set_image_url(image_url)
        self.set_followers(followers)
        self.set_timestamp(timestamp)
        # API
        self.set_token(token)

    # ---- Getter Functions ----

    def get_id(self) -> str:
        return self.id

    def get_display_name(self) -> str:
        return self.display_name

    def get_image_url(self) -> str:
        return self.image_url

    def get_followers(self) -> int:
        return self.followers

    def get_timestamp(self) -> int:
        return self.timestamp
    
    def get_token(self) -> dict:
        if not self.has_token():
            return {"access_token":"","token_type":"","expires_in":"","scope":"","expires_at":"","refresh_token":""}
        else:
            return self.token
        
    # ---- Setter Functions ----

    def set_id(self, id: str):
        self.id = id 
    
    def set_display_name(self, name: str):
        self.display_name = name

    def set_image_url(self, url: str):
        self.image_url = url
        
    def set_followers(self, followers: int):
        self.followers = followers

    def set_timestamp(self, timestamp: int):
        self.timestamp = timestamp
        
    def set_token(self, token: dict):
        self.token = token

    # ---- Other Functions ----
    
    def merge(self, other: 'User') -> 'User':
        """Merges another user object into this one. Newest non-None information will be kept.

        Args:
            other (User): User to merge into this object
        """
        # Check input
        if not isinstance(other, User):
            raise TypeError
        if self.get_id() != other.get_id():
            self.logger.error("Cannot merge two different user-ids!")
            return
        # Determine who has newer data
        if self.get_timestamp() < other.get_timestamp():
            new = other
            old = self
        else:
            new = self
            old = other
        # display name
        if new.get_display_name() is None:
            self.set_display_name(old.get_display_name())
        else:
            self.set_display_name(new.get_display_name())
        # image url
        if new.get_image_url() is None:
            self.set_image_url(old.get_image_url())
        else:
            self.set_image_url(new.get_image_url())
        # followers
        if new.get_followers() is None:
            self.set_followers(old.get_followers())
        else:
            self.set_followers(new.get_followers())
        # timestamp
        self.set_timestamp(new.get_timestamp())
        # token
        if new.has_token():
            self.set_token(new.get_token())
        elif old.has_token():
            self.set_token(old.get_token())
        return self
    
    def has_token(self) -> bool:
        """
        Checks if user contains usable token

        Returns:
            bool: token usable
        """
        if self.token is None:
            return False
        required_keys = ["access_token","token_type","expires_in","scope","expires_at","refresh_token"]
        for key in required_keys:
            if key not in self.token:
                return False
        return True