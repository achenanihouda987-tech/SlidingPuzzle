import unittest
from models.board_model import BoardModel
from services.movement_service import MovementService
from services.shuffle_service import ShuffleService
from services.victory_service import VictoryService

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.board = BoardModel(3)
        
    def test_solved_state(self):
        self.assertTrue(VictoryService.check_victory(self.board))
        
    def test_valid_move(self):
        # Initial empty is at 8. 5 and 7 are adjacent.
        self.assertTrue(MovementService.is_adjacent(self.board, 5, 8))
        move = MovementService.move(self.board, 5)
        self.assertIsNotNone(move)
        self.assertFalse(VictoryService.check_victory(self.board))
        
    def test_invalid_move(self):
        # 0 is not adjacent to 8
        self.assertFalse(MovementService.is_adjacent(self.board, 0, 8))
        move = MovementService.move(self.board, 0)
        self.assertIsNone(move)
        
    def test_shuffle_makes_unsolved(self):
        ShuffleService.shuffle(self.board, num_moves=50)
        self.assertFalse(VictoryService.check_victory(self.board))

if __name__ == '__main__':
    unittest.main()
