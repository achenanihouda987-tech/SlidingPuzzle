from dataclasses import dataclass, field
from typing import List

from models.move_model import MoveModel

@dataclass
class GameState:
    """
    Encapsulates the global state of an active puzzle session.
    It isolates session variables (like time, moves, and history) from the rules and UI.
    """
    is_playing: bool = False
    moves_count: int = 0
    time_seconds: int = 0
    move_history: List[MoveModel] = field(default_factory=list)

    def reset(self) -> None:
        """
        Resets the state for a brand new game.
        """
        self.is_playing = True
        self.moves_count = 0
        self.time_seconds = 0
        self.move_history.clear()

    def add_move(self, move: MoveModel) -> None:
        """
        Records a move and increments the global move counter.
        """
        self.move_history.append(move)
        self.moves_count += 1

    def tick_time(self) -> None:
        """
        Increments the session's play time.
        """
        if self.is_playing:
            self.time_seconds += 1

    def stop(self) -> None:
        """
        Halts the active game state (e.g., upon victory).
        """
        self.is_playing = False
