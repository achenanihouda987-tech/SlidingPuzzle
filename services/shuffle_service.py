import random
from models.board_model import BoardModel

class ShuffleService:
    """
    Ensures the puzzle is always solvable by shuffling via legal moves
    starting from a solved state.
    """
    @staticmethod
    def shuffle(board: BoardModel, num_moves: int = 500) -> None:
        board.initialize_solved()
        last_empty = -1
        size = board.size
        
        for _ in range(num_moves):
            empty_idx = board.get_empty_index()
            possible_moves = []
            
            # Manual adjacency check is much faster than looping the whole board
            r, c = divmod(empty_idx, size)
            if r > 0: possible_moves.append(empty_idx - size) # Up
            if r < size - 1: possible_moves.append(empty_idx + size) # Down
            if c > 0: possible_moves.append(empty_idx - 1) # Left
            if c < size - 1: possible_moves.append(empty_idx + 1) # Right
            
            # Prevent useless immediate backtracking (A -> B -> A)
            if len(possible_moves) > 1 and last_empty in possible_moves:
                possible_moves.remove(last_empty)
                
            choice = random.choice(possible_moves)
            board.swap_positions(empty_idx, choice)
            last_empty = empty_idx
