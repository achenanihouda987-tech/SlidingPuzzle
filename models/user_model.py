from dataclasses import dataclass


@dataclass
class UserModel:
    """Represents an authenticated user."""
    id: int
    username: str
    email: str
    created_at: str
