from __future__ import annotations
from typing import Optional, List
from database import db_manager


def insert(user_id: int, theme: str, difficulty: int,
           moves: int, time_seconds: int, score: int) -> None:
    conn = db_manager.get_connection()
    try:
        conn.execute(
            """INSERT INTO BestScores
               (user_id, theme, difficulty, moves, time_seconds, score)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, theme, difficulty, moves, time_seconds, score),
        )
        conn.commit()
    finally:
        conn.close()


def get_best_score_for_user(user_id: int, difficulty: int) -> Optional[int]:
    """Returns the highest score for the user at the given difficulty."""
    conn = db_manager.get_connection()
    try:
        row = conn.execute(
            """SELECT MAX(score) as best FROM BestScores
               WHERE user_id=? AND difficulty=?""",
            (user_id, difficulty),
        ).fetchone()
        return row["best"] if row and row["best"] is not None else None
    finally:
        conn.close()


def get_history_for_user(user_id: int) -> List[dict]:
    conn = db_manager.get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM BestScores WHERE user_id=?
               ORDER BY score DESC""",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_user_stats(user_id: int) -> dict:
    """Returns total games played, total wins (all scores), and best score."""
    conn = db_manager.get_connection()
    try:
        row = conn.execute(
            """SELECT 
                 (SELECT games_played FROM Users WHERE id=?) as total_games,
                 COUNT(*) as total_wins, 
                 MAX(score) as best_score
               FROM BestScores WHERE user_id=?""",
            (user_id, user_id),
        ).fetchone()
        return {
            "total_games": row["total_games"] or 0,
            "total_wins": row["total_wins"] or 0,
            "best_score": row["best_score"] or 0,
        }
    finally:
        conn.close()
