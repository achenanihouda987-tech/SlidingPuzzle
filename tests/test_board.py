import unittest
from models.board_model import BoardModel
from services.movement_service import MovementService

class TestBoardModel(unittest.TestCase):
    def setUp(self):
        self.board = BoardModel(3)
        
    def test_initial_state(self):
        self.assertEqual(len(self.board.grid), 9)
        self.assertTrue(self.board.grid[-1].is_empty)
        
    def test_adjacency(self):
        self.assertTrue(MovementService.is_adjacent(self.board, 4, 1))
        self.assertTrue(MovementService.is_adjacent(self.board, 4, 3))
        self.assertTrue(MovementService.is_adjacent(self.board, 4, 5))
        self.assertTrue(MovementService.is_adjacent(self.board, 4, 7))
        self.assertFalse(MovementService.is_adjacent(self.board, 4, 0)) # Diagonal
        self.assertFalse(MovementService.is_adjacent(self.board, 4, 8)) # Diagonal
        self.assertFalse(MovementService.is_adjacent(self.board, 0, 2)) # Far

if __name__ == '__main__':
    unittest.main()
