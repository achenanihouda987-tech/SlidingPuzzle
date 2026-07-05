from models.board_model import BoardModel

class VictoryService:
    """
    Encapsulates victory logic. Kept lightweight as BoardModel already provides O(N) checking.
    """
    @staticmethod
    def check_victory(board: BoardModel) -> bool:
        """
        Returns True if the board is fully solved.
        """
        return board.is_solved()
