from __future__ import annotations
import hashlib
import os
import binascii
from typing import Optional
from database import db_manager
from models.user_model import UserModel


def _hash_password(password: str, salt: bytes) -> str:
    """Returns a PBKDF2-HMAC-SHA256 hex digest."""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260_000)
    return binascii.hexlify(dk).decode("ascii")


def create_user(username: str, email: str, password_hash: str, salt: str) -> UserModel:
    conn = db_manager.get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO Users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, salt),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM Users WHERE id = ?", (cur.lastrowid,)).fetchone()
        return UserModel(id=row["id"], username=row["username"],
                         email=row["email"], created_at=row["created_at"])
    finally:
        conn.close()


def find_by_username(username: str) -> Optional[dict]:
    conn = db_manager.get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def find_by_email(email: str) -> Optional[dict]:
    conn = db_manager.get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM Users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def verify_password(plain: str, stored_hash: str, salt_hex: str) -> bool:
    salt = binascii.unhexlify(salt_hex)
    return _hash_password(plain, salt) == stored_hash


def make_salt() -> bytes:
    return os.urandom(32)


def increment_games_played(user_id: int) -> None:
    conn = db_manager.get_connection()
    try:
        conn.execute(
            "UPDATE Users SET games_played = games_played + 1 WHERE id = ?",
            (user_id,)
        )
        conn.commit()
    finally:
        conn.close()
