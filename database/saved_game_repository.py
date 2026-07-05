from __future__ import annotations
import json
from typing import Optional
from database import db_manager


def upsert(user_id: int, theme: str, difficulty: int,
           moves: int, elapsed_time: int,
           board_state: list, progress: int) -> None:
    """Insert or replace the single saved game for this user."""
    state_json = json.dumps(board_state)
    conn = db_manager.get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM SavedGames WHERE user_id = ?", (user_id,)
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE SavedGames
                   SET theme=?, difficulty=?, moves=?, elapsed_time=?,
                       board_state=?, progress=?, last_played=datetime('now')
                   WHERE user_id=?""",
                (theme, difficulty, moves, elapsed_time, state_json, progress, user_id),
            )
        else:
            conn.execute(
                """INSERT INTO SavedGames
                   (user_id, theme, difficulty, moves, elapsed_time, board_state, progress)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, theme, difficulty, moves, elapsed_time, state_json, progress),
            )
        conn.commit()
    finally:
        conn.close()


def find_by_user(user_id: int) -> Optional[dict]:
    conn = db_manager.get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM SavedGames WHERE user_id = ?", (user_id,)
        ).fetchone()
        if row:
            d = dict(row)
            d["board_state"] = json.loads(d["board_state"])
            return d
        return None
    finally:
        conn.close()


def delete(user_id: int) -> None:
    conn = db_manager.get_connection()
    try:
        conn.execute("DELETE FROM SavedGames WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()
