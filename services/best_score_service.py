from __future__ import annotations
from typing import Optional
from database import score_repository


class BestScoreService:
    """
    Handles all operations related to best score computation and persistence.
    Score Formula: (1000 - moves*5 - time_seconds) * difficulty_multiplier
      3×3 → ×1 | 4×4 → ×2 | 5×5 → ×3
    """
    DIFFICULTY_MULTIPLIER = {3: 1, 4: 2, 5: 3}

    @classmethod
    def calculate_score(cls, moves: int, time_seconds: int, difficulty: int) -> int:
        multiplier = cls.DIFFICULTY_MULTIPLIER.get(difficulty, 1)
        raw = max(0, 1000 - moves * 5 - time_seconds)
        return raw * multiplier

    @classmethod
    def save_if_record(cls, user_id: int, theme: str, difficulty: int,
                       moves: int, time_seconds: int) -> tuple[int, bool]:
        """
        Calculates score and saves it. Always saves (to build history).
        Returns (score, is_new_record).
        """
        score = cls.calculate_score(moves, time_seconds, difficulty)
        current_best = score_repository.get_best_score_for_user(user_id, difficulty)
        is_record = (current_best is None or score > current_best)
        score_repository.insert(user_id, theme, difficulty, moves, time_seconds, score)
        return score, is_record

    @classmethod
    def get_best(cls, user_id: int, difficulty: int) -> Optional[int]:
        return score_repository.get_best_score_for_user(user_id, difficulty)
