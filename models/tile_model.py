from dataclasses import dataclass

@dataclass(frozen=True)
class TileModel:
    """
    Represents a single puzzle piece in the game.
    Uses frozen=True to enforce immutability, ensuring that a tile's core
    identity never changes throughout its lifecycle.
    """
    id: int
    is_empty: bool
