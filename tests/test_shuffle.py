import unittest
from models.board_model import BoardModel
from services.shuffle_service import ShuffleService
from services.victory_service import VictoryService

class TestShuffle(unittest.TestCase):
    def test_shuffle(self):
        board = BoardModel(3)
        ShuffleService.shuffle(board, 100)
        self.assertFalse(VictoryService.check_victory(board))
        
if __name__ == '__main__':
    unittest.main()
