from typing import Tuple
from models.board_model import BoardModel
from models.move_model import MoveModel

class MovementService:
    """
    Handles the validation and execution of tile movements.
    """
    @staticmethod
    def is_adjacent(board: BoardModel, idx1: int, idx2: int) -> bool:
        """
        Checks if two indices are strictly adjacent (up, down, left, right).
        Diagonals are invalid.
        """
        size = board.size
        r1, c1 = divmod(idx1, size)
        r2, c2 = divmod(idx2, size)
        return abs(r1 - r2) + abs(c1 - c2) == 1

    @staticmethod
    def move(board: BoardModel, target_idx: int) -> MoveModel | None:
        """
        Attempts to move the tile at target_idx to the empty spot.
        Returns a MoveModel if successful, None otherwise.
        """
        empty_idx = board.get_empty_index()
        if MovementService.is_adjacent(board, target_idx, empty_idx):
            board.swap_positions(target_idx, empty_idx)
            # Find which tile just moved (it is now at empty_idx)
            tile = board.get_tile_at(empty_idx)
            return MoveModel(tile_id=tile.id, from_idx=target_idx, to_idx=empty_idx)
        return None
