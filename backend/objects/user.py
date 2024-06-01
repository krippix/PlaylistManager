from dataclasses import dataclass


@dataclass
class User:
    """
    Represents user in database
    """
    user_id: str = None
    display_name: str = None
    email: str = None
    confirmed: bool = None
    access_token: str = None
    token_type: str = None
    expires_in: int = None
    refresh_token: str = None
    scope: str = None
    expires_at: int = None
