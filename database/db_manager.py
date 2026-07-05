import sqlite3
import os
from pathlib import Path


def _get_db_path() -> str:
    """Returns path to the SQLite database file, creating directory if needed."""
    db_dir = Path.home() / ".sliding_puzzle"
    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / "game.db")


def get_connection() -> sqlite3.Connection:
    """Returns a new SQLite connection with row_factory set."""
    conn = sqlite3.connect(_get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize() -> None:
    """Creates all database tables on first launch if they do not exist."""
    conn = get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS Users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                email         TEXT    NOT NULL UNIQUE,
                password_hash TEXT    NOT NULL,
                salt          TEXT    NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS SavedGames (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                theme        TEXT    NOT NULL,
                difficulty   INTEGER NOT NULL,
                moves        INTEGER NOT NULL DEFAULT 0,
                elapsed_time INTEGER NOT NULL DEFAULT 0,
                board_state  TEXT    NOT NULL,
                progress     INTEGER NOT NULL DEFAULT 0,
                last_played  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS BestScores (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                theme        TEXT    NOT NULL,
                difficulty   INTEGER NOT NULL,
                moves        INTEGER NOT NULL,
                time_seconds INTEGER NOT NULL,
                score        INTEGER NOT NULL,
                date_created TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)
        
        # Safe migration for existing DB
        try:
            conn.execute("ALTER TABLE Users ADD COLUMN games_played INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass # Column already exists
            
        conn.commit()
    finally:
        conn.close()
