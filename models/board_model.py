from typing import List

from models.tile_model import TileModel

class BoardModel:
    """
    Represents the grid logic and state of the puzzle board.
    Optimized for O(1) lookups both by grid index and by tile ID.
    """
    def __init__(self, size: int):
        """
        Initializes an empty board model of given size NxN.
        """
        if size < 3:
            raise ValueError("Board size must be at least 3x3")
            
        self.size = size
        self.total_tiles = size * size
        self.empty_tile_id = self.total_tiles - 1
        
        # grid[position_index] = TileModel
        self.grid: List[TileModel] = []
        
        # tile_positions[tile_id] = position_index
        # This provides O(1) lookup to find where a specific tile currently is.
        self.tile_positions: List[int] = [0] * self.total_tiles
        
        self.initialize_solved()

    def initialize_solved(self) -> None:
        """
        Populates the board in its perfectly solved state.
        The last tile is always designated as the empty tile.
        """
        self.grid.clear()
        for i in range(self.total_tiles):
            is_empty = (i == self.empty_tile_id)
            tile = TileModel(id=i, is_empty=is_empty)
            self.grid.append(tile)
            self.tile_positions[i] = i

    def get_tile_at(self, index: int) -> TileModel:
        """
        O(1) retrieval of the tile currently at a specific grid index.
        """
        return self.grid[index]

    def get_position_of(self, tile_id: int) -> int:
        """
        O(1) retrieval of the current grid index of a specific tile ID.
        """
        return self.tile_positions[tile_id]

    def get_empty_index(self) -> int:
        """
        O(1) retrieval of the empty tile's current grid index.
        """
        return self.get_position_of(self.empty_tile_id)

    def swap_positions(self, index1: int, index2: int) -> None:
        """
        Swaps the tiles at index1 and index2.
        Updates both the grid state and the O(1) position lookup array.
        """
        tile1 = self.grid[index1]
        tile2 = self.grid[index2]
        
        # Swap in grid
        self.grid[index1], self.grid[index2] = tile2, tile1
        
        # Update quick lookup
        self.tile_positions[tile1.id] = index2
        self.tile_positions[tile2.id] = index1

    def is_solved(self) -> bool:
        """
        Checks if every tile is at its correct target position.
        """
        for index, tile in enumerate(self.grid):
            if tile.id != index:
                return False
        return True

    def clone(self) -> 'BoardModel':
        """
        Creates a deep copy of the board model state.
        Useful for simulating moves or AI solving.
        """
        cloned = BoardModel(self.size)
        cloned.grid = self.grid.copy()
        cloned.tile_positions = self.tile_positions.copy()
        return cloned
