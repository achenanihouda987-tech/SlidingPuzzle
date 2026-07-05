from models.board_model import BoardModel

class BoardService:
    """
    Manages the creation and lifecycle of the BoardModel.
    """
    @staticmethod
    def create_board(size: int) -> BoardModel:
        return BoardModel(size)
