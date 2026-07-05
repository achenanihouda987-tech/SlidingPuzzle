from __future__ import annotations
from typing import Optional
from models.user_model import UserModel


class SessionService:
    """
    Singleton that holds the currently logged-in user for the session.
    Access via SessionService.instance().
    """
    _instance: Optional["SessionService"] = None
    current_user: Optional[UserModel] = None

    @classmethod
    def instance(cls) -> "SessionService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def login(self, user: UserModel) -> None:
        self.current_user = user

    def logout(self) -> None:
        self.current_user = None

    def is_logged_in(self) -> bool:
        return self.current_user is not None

    def get_user(self) -> Optional[UserModel]:
        return self.current_user
