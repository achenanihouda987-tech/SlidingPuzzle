from __future__ import annotations
import binascii
from typing import Optional
from database import user_repository
from models.user_model import UserModel


class AuthService:
    """Handles user registration and login with PBKDF2-hashed passwords."""

    @staticmethod
    def register(username: str, email: str, password: str) -> UserModel:
        """
        Creates a new user account.
        Raises ValueError if username or email already exists.
        """
        username = username.strip()
        email = email.strip().lower()

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if "@" not in email or "." not in email:
            raise ValueError("Please enter a valid email address.")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        if user_repository.find_by_username(username):
            raise ValueError(f"Username '{username}' is already taken.")
        if user_repository.find_by_email(email):
            raise ValueError(f"Email '{email}' is already registered.")

        salt = user_repository.make_salt()
        salt_hex = binascii.hexlify(salt).decode("ascii")
        pw_hash = user_repository._hash_password(password, salt)

        return user_repository.create_user(username, email, pw_hash, salt_hex)

    @staticmethod
    def login(username_or_email: str, password: str) -> Optional[UserModel]:
        """
        Attempts to authenticate a user.
        Returns UserModel on success, None on failure.
        """
        identifier = username_or_email.strip()

        # Try username first, then email
        row = user_repository.find_by_username(identifier)
        if not row:
            row = user_repository.find_by_email(identifier.lower())
        if not row:
            return None

        if not user_repository.verify_password(password, row["password_hash"], row["salt"]):
            return None

        return UserModel(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            created_at=row["created_at"],
        )
